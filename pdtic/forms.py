from django import forms
from .models import PDTIC, VersaoPDTIC


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


class VersaoPDTICForm(forms.ModelForm):
    class Meta:
        model = VersaoPDTIC
        fields = ["numero_versao", "data_aprovacao", "documento", "observacoes"]
        widgets = {
            'numero_versao': forms.TextInput(attrs={
                'class': 'block w-full h-12 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-600 sm:text-sm text-gray-900 placeholder-gray-400',
                'placeholder': 'Ex: v1.0, v2.0'
            }),
            'data_aprovacao': forms.DateInput(attrs={
                'class': 'block w-full h-12 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-600 sm:text-sm text-gray-900',
                'type': 'date'
            }),
            'documento': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-md cursor-pointer bg-gray-50 focus:outline-none focus:border-primary-600'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'block w-full border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-600 sm:text-sm text-gray-900 placeholder-gray-400',
                'rows': 4,
                'placeholder': 'Observações sobre esta versão...'
            }),
        }
