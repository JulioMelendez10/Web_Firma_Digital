from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Documento
from .forms import DocumentoForm, DocumentoEditarForm
import os

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
    
    context = {
        'page_obj': page_obj,
        'total_documentos': total_documentos,
        'documentos_firmados': documentos_firmados,
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
    return render(request, 'documentos/detalle.html', {'documento': documento})

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