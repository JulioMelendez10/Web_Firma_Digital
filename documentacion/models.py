from django.db import models
from django.contrib.auth.models import User
import hashlib
import os

class Documento(models.Model):
    """Modelo para gestionar documentos digitales"""
    
    # Campos del documento
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    # Archivo
    archivo = models.FileField(upload_to='documentos/', verbose_name="Archivo")
    
    # Usuario propietario
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='documentos',
        verbose_name="Propietario"
    )
    
    # Hash del documento
    hash_sha256 = models.CharField(max_length=64, blank=True, verbose_name="Hash SHA-256")
    
    # Fechas
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de carga")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    # Estado
    esta_firmado = models.BooleanField(default=False, verbose_name="¿Está firmado?")
    
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ['-fecha_carga']
    
    def __str__(self):
        return self.titulo
    
    def calcular_hash(self):
        """Calcula el hash SHA-256 del archivo"""
        if self.archivo and os.path.exists(self.archivo.path):
            sha256_hash = hashlib.sha256()
            with open(self.archivo.path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        return None
    
    def guardar_con_hash(self, *args, **kwargs):
        """Guarda el documento y calcula su hash automáticamente"""
        super().save(*args, **kwargs)
        hash_calculado = self.calcular_hash()
        if hash_calculado:
            self.hash_sha256 = hash_calculado
            super().save(update_fields=['hash_sha256'])
    
    def save(self, *args, **kwargs):
        """Sobreescribe el método save para manejar el hash"""
        if not self.pk or (self.pk and 'archivo' in kwargs.get('update_fields', [])):
            super().save(*args, **kwargs)
            self.guardar_con_hash()
        else:
            super().save(*args, **kwargs)
    
    def get_tamaño(self):
        """Retorna el tamaño del archivo en formato legible"""
        if self.archivo and os.path.exists(self.archivo.path):
            size = os.path.getsize(self.archivo.path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
        return "0 B"
    
    def get_extension(self):
        """Retorna la extensión del archivo"""
        if self.archivo:
            return os.path.splitext(self.archivo.name)[1].lower()
        return ""