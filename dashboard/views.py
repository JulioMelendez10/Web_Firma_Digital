from django.shortcuts import render

from certificates.models import Certificado
from documentacion.models import Documento


def home(request):
    total_documentos = Documento.objects.count()
    documentos_firmados = Documento.objects.filter(esta_firmado=True).count()
    documentos_por_firmar = Documento.objects.filter(esta_firmado=False).count()
    certificados_totales = Certificado.objects.count()

    ultimos_documentos = Documento.objects.order_by('-fecha_carga')[:5]
    documentos_pendientes = Documento.objects.filter(esta_firmado=False).order_by('-fecha_carga')[:5]

    context = {
        'title': 'Panel principal',
        'total_documentos': total_documentos,
        'documentos_firmados': documentos_firmados,
        'documentos_por_firmar': documentos_por_firmar,
        'certificados_totales': certificados_totales,
        'ultimos_documentos': ultimos_documentos,
        'documentos_pendientes': documentos_pendientes,
    }

    return render(request, 'dashboard/home.html', context)
