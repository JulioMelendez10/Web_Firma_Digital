import hashlib
import re

from cryptography import x509
from cryptography.hazmat.primitives import hashes

from django.shortcuts import render, redirect

from .forms import CertificadoForm
from .models import Certificado


def extraer_datos_certificado(archivo):

    contenido = archivo.read()

    try:
        certificado = x509.load_der_x509_certificate(contenido)
    except Exception:
        certificado = x509.load_pem_x509_certificate(contenido)

    subject = certificado.subject.rfc4514_string()
    issuer = certificado.issuer.rfc4514_string()

    rfc = ''
    curp = ''

    texto = subject

    rfc_match = re.search(
        r'[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}',
        texto
    )

    curp_match = re.search(
        r'[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]{2}',
        texto
    )

    if rfc_match:
        rfc = rfc_match.group()

    if curp_match:
        curp = curp_match.group()

    return {
        'numero_serie': str(certificado.serial_number),
        'subject': subject,
        'issuer': issuer,
        'rfc': rfc,
        'curp': curp,
        'fecha_inicio': certificado.not_valid_before_utc,
        'fecha_expiracion': certificado.not_valid_after_utc,
        'algoritmo_firma': certificado.signature_hash_algorithm.name,
        'huella_sha256': certificado.fingerprint(
            hashes.SHA256()
        ).hex().upper(),
    }


def certificate_list(request):

    certificados = Certificado.objects.all().order_by(
        '-fecha_registro'
    )

    if request.method == 'POST':

        form = CertificadoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            certificado_obj = form.save(commit=False)

            datos = extraer_datos_certificado(
                request.FILES['archivo_cer']
            )

            certificado_obj.numero_serie = datos['numero_serie']
            certificado_obj.subject = datos['subject']
            certificado_obj.issuer = datos['issuer']
            certificado_obj.rfc = datos['rfc']
            certificado_obj.curp = datos['curp']
            certificado_obj.fecha_inicio = datos['fecha_inicio']
            certificado_obj.fecha_expiracion = datos['fecha_expiracion']
            certificado_obj.algoritmo_firma = datos['algoritmo_firma']
            certificado_obj.huella_sha256 = datos['huella_sha256']

            certificado_obj.save()

            return redirect('certificates')

    else:
        form = CertificadoForm()

    return render(
        request,
        'certificates/list.html',
        {
            'title': 'Certificados',
            'form': form,
            'certificados': certificados,
        }
    )