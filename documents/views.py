import os
import mimetypes
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DocumentoEditarForm, DocumentoForm
from .models import Documento


@login_required
def lista_documentos(request):
    documentos = Documento.objects.filter(usuario=request.user).order_by('-fecha_carga')

    query = request.GET.get('q')
    if query:
        documentos = documentos.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query))

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
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.usuario = request.user
            documento.save()
            messages.success(request, f'Documento "{documento.titulo}" creado exitosamente.')
            return redirect('documentos:detalle', pk=documento.pk)
        messages.error(request, 'Error al crear el documento.')
    else:
        form = DocumentoForm()

    return render(request, 'documentos/crear.html', {'form': form})


@login_required
def detalle_documento(request, pk):
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)
    return render(request, 'documentos/detalle.html', {'documento': documento})


@login_required
def editar_documento(request, pk):
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)

    if request.method == 'POST':
        form = DocumentoEditarForm(request.POST, instance=documento)
        if form.is_valid():
            form.save()
            messages.success(request, f'Documento "{documento.titulo}" actualizado correctamente.')
            return redirect('documentos:detalle', pk=documento.pk)
    else:
        form = DocumentoEditarForm(instance=documento)

    return render(request, 'documentos/editar.html', {'form': form, 'documento': documento})


@login_required
def eliminar_documento(request, pk):
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
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)

    if documento.archivo and os.path.exists(documento.archivo.path):
        content_type, _ = mimetypes.guess_type(documento.archivo.name)
        response = FileResponse(
            documento.archivo.open('rb'),
            as_attachment=True,
            filename=os.path.basename(documento.archivo.name),
            content_type=content_type or 'application/octet-stream',
        )
        return response

    messages.error(request, 'El archivo no existe en el servidor.')
    return redirect('documentos:detalle', pk=documento.pk)


@login_required
def verificar_hash(request, pk):
    documento = get_object_or_404(Documento, pk=pk, usuario=request.user)
    hash_actual = documento.calcular_hash()
    hash_guardado = documento.hash_sha256

    if hash_actual and hash_guardado:
        if hash_actual == hash_guardado:
            messages.success(request, 'El documento no ha sido modificado.')
        else:
            messages.error(request, 'Advertencia: el documento ha sido modificado.')
    else:
        messages.warning(request, 'No se pudo verificar el hash.')

    return redirect('documentos:detalle', pk=documento.pk)
