from django.contrib import admin
from .models import Certificado


@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'numero_serie',
        'rfc',
        'fecha_expiracion',
        'fecha_registro',
    )

    search_fields = (
        'numero_serie',
        'rfc',
        'curp',
    )