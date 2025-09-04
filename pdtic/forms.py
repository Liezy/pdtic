from django import forms
from .models import PDTIC


class PDTICForm(forms.ModelForm):
    class Meta:
        model = PDTIC
        fields = ["instituicao", "titulo", "descricao", "vigencia_inicio", "vigencia_fim", "status"]
        widgets = {
            'instituicao': forms.Select(attrs={
                'class': 'block w-full h-12 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-600 sm:text-sm text-gray-900'
            }),
            'status': forms.Select(attrs={
                'class': 'block w-full h-12 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-600 sm:text-sm text-gray-900'
            }),
        }
