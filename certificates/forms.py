from django import forms
from .models import Certificado


class CertificadoForm(forms.ModelForm):

    class Meta:
        model = Certificado
        fields = ['archivo_cer', 'archivo_key']

    def clean_archivo_cer(self):
        archivo = self.cleaned_data['archivo_cer']

        if not archivo.name.lower().endswith('.cer'):
            raise forms.ValidationError(
                'Solo se permiten archivos .cer'
            )

        return archivo

    def clean_archivo_key(self):
        archivo = self.cleaned_data['archivo_key']

        if not archivo.name.lower().endswith('.key'):
            raise forms.ValidationError(
                'Solo se permiten archivos .key'
            )

        return archivo