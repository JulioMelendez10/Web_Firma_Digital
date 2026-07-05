from django import forms
import os
from .models import Documento


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'descripcion', 'archivo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título del documento',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ingrese una descripción (opcional)',
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt,.jpg,.jpeg,.png',
            }),
        }

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if not archivo:
            return archivo

        if archivo.size > 10 * 1024 * 1024:
            raise forms.ValidationError('El archivo no puede exceder los 10MB.')

        extensiones_permitidas = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png']
        ext = os.path.splitext(archivo.name)[1].lower()
        if ext not in extensiones_permitidas:
            raise forms.ValidationError(f"Extensión '{ext}' no permitida.")

        return archivo


class DocumentoEditarForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título del documento',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ingrese una descripción (opcional)',
            }),
        }