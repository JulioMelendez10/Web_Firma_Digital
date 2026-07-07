from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from documentacion.models import Documento


@login_required
def signature_list(request):
    firmas = Documento.objects.filter(usuario=request.user, esta_firmado=True).order_by('-fecha_firma')
    return render(request, 'signatures/list.html', {
        'title': 'Firmas digitales',
        'firmas': firmas,
    })
