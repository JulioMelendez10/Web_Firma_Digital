from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from documentacion.models import Documento


@login_required
def history_list(request):
    documentos = Documento.objects.filter(usuario=request.user).order_by('-fecha_carga')
    return render(request, 'logs/list.html', {
        'title': 'Historial de documentos',
        'documentos': documentos,
    })
