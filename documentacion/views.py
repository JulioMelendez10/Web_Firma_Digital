import os
import base64
import hashlib

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from certificates.models import Certificado
from .models import Documento
from .forms import DocumentoForm, DocumentoEditarForm

@login_required
def lista_documentos(request):
    """Vista para listar todos los documentos del usuario"""
    documentos = Documento.objects.filter(usuario=request.user).order_by('-fecha_carga')
    
    query = request.GET.get('q')
    if query:
        documentos = documentos.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        )
    
    paginator = Paginator(documentos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_documentos = documentos.count()
    documentos_firmados = documentos.filter(esta_firmado=True).count()
    documentos_por_firmar = total_documentos - documentos_firmados
    
    context = {
        'page_obj': page_obj,
        'total_documentos': total_documentos,
        'documentos_firmados': documentos_firmados,
        'documentos_por_firmar': documentos_por_firmar,
        'query': query,
    }
    return render(request, 'documentos/lista.html', context)

@login_required
def crear_documento(request):
    """Vista para crear un nuevo documento"""
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.usuario = request.user
            documento.guardar_con_hash()
            messages.success(request, f'Documento "{documento.titulo}" creado exitosamente.')
            return redirect('documentos:detalle', pk=documento.pk)
        else:
            messages.error(request, 'Error al crear el documento.')
    else:
        form = DocumentoForm()
    
    return render(request, 'documentos/crear.html', {'form': form})

@login_required
def detalle_documento(request, pk):
    """Vista para ver el detalle de un documento"""
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)
    certificados = Certificado.objects.order_by('-fecha_registro')
    return render(
        request,
        'documentos/detalle.html',
        {
            'documento': documento,
            'certificados': certificados,
        }
    )

@login_required
def firmar_documento(request, pk):
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)

    if request.method != 'POST':
        return redirect('documentos:detalle', pk=documento.pk)

    certificado_id = request.POST.get('certificado_id')
    key_password = request.POST.get('key_password', '').strip()
    certificado = get_object_or_404(Certificado, pk=certificado_id)

    hash_val = documento.calcular_hash()
    if not hash_val:
        messages.error(request, 'No se pudo calcular el hash del documento.')
        return redirect('documentos:detalle', pk=documento.pk)

    try:
        with open(certificado.archivo_key.path, 'rb') as key_file:
            key_data = key_file.read()

        password = key_password.encode('utf-8') if key_password else None
        private_key = serialization.load_pem_private_key(
            key_data,
            password=password,
        )

        signature = private_key.sign(
            hash_val.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        documento.certificado = certificado
        documento.firma_sha256 = base64.b64encode(signature).decode('utf-8')
        documento.esta_firmado = True
        documento.fecha_firma = timezone.now()
        documento.save()

        messages.success(request, 'Documento firmado correctamente.')
    except (TypeError, ValueError) as err:
        messages.error(
            request,
            'Error al firmar el documento. Verifica la contraseña de la llave privada o que el archivo .key sea compatible.'
        )
    except Exception as err:
        messages.error(request, f'Error al firmar el documento: {err}')

    return redirect('documentos:detalle', pk=documento.pk)

@login_required
def verificar_firma(request, pk):
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)

    if not documento.firma_sha256 or not documento.certificado:
        messages.warning(request, 'Este documento no tiene firma digital asociada.')
        return redirect('documentos:detalle', pk=documento.pk)

    try:
        with open(documento.certificado.archivo_cer.path, 'rb') as cert_file:
            cert_data = cert_file.read()

        try:
            certificado_obj = x509.load_pem_x509_certificate(cert_data)
        except Exception:
            certificado_obj = x509.load_der_x509_certificate(cert_data)

        public_key = certificado_obj.public_key()
        signature = base64.b64decode(documento.firma_sha256.encode('utf-8'))
        hash_val = documento.calcular_hash()

        public_key.verify(
            signature,
            hash_val.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        messages.success(request, 'La firma digital del documento es válida.')
    except Exception as err:
        messages.error(request, f'La firma digital no es válida: {err}')

    return redirect('documentos:detalle', pk=documento.pk)

@login_required
def editar_documento(request, pk):
    """Vista para editar un documento"""
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = DocumentoEditarForm(request.POST, instance=documento)
        if form.is_valid():
            form.save()
            messages.success(request, f'Documento "{documento.titulo}" actualizado correctamente.')
            return redirect('documentos:detalle', pk=documento.pk)
    else:
        form = DocumentoEditarForm(instance=documento)
    
    return render(request, 'documentos/editar.html', {
        'form': form,
        'documento': documento
    })

@login_required
def eliminar_documento(request, pk):
    """Vista para eliminar un documento"""
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        titulo = documento.titulo
        if documento.archivo and os.path.exists(documento.archivo.path):
            os.remove(documento.archivo.path)
        documento.delete()
        messages.success(request, f'Documento "{titulo}" eliminado exitosamente.')
        return redirect('documentos:lista')
    
    return render(request, 'documentos/eliminar.html', {'documento': documento})

@login_required
def descargar_documento(request, pk):
    """Vista para descargar un documento"""
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)
    
    if documento.archivo and os.path.exists(documento.archivo.path):
        with open(documento.archivo.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{documento.archivo.name}"'
            return response
    else:
        messages.error(request, 'El archivo no existe en el servidor.')
        return redirect('documentos:detalle', pk=documento.pk)

@login_required
def verificar_hash(request, pk):
    """Vista para verificar la integridad del documento"""
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)
    
    hash_actual = documento.calcular_hash()
    hash_guardado = documento.hash_sha256
    
    if hash_actual and hash_guardado:
        if hash_actual == hash_guardado:
            messages.success(request, '✅ El documento NO ha sido modificado.')
        else:
            messages.error(request, '⚠️ ¡ADVERTENCIA! El documento ha sido modificado.')
    else:
        messages.warning(request, 'No se pudo verificar el hash.')
    
    return redirect('documentos:detalle', pk=documento.pk)