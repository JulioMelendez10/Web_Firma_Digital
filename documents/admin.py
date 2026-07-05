from django.contrib import admin
from .models import Documento


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'usuario', 'fecha_carga', 'esta_firmado')
	list_filter = ('esta_firmado', 'fecha_carga')
	search_fields = ('titulo', 'descripcion', 'usuario__username')

# Register your models here.
