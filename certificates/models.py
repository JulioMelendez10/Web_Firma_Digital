from django.db import models


class Certificado(models.Model):
    archivo_cer = models.FileField(upload_to='certificados/cer/')
    archivo_key = models.FileField(upload_to='certificados/key/')

    numero_serie = models.CharField(max_length=255, blank=True)
    subject = models.TextField(blank=True)
    issuer = models.TextField(blank=True)

    rfc = models.CharField(max_length=20, blank=True)
    curp = models.CharField(max_length=30, blank=True)

    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_expiracion = models.DateTimeField(null=True, blank=True)

    algoritmo_firma = models.CharField(max_length=255, blank=True)
    huella_sha256 = models.CharField(max_length=255, blank=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'

    def __str__(self):
        return self.numero_serie or f'Certificado {self.id}'