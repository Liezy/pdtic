from django import forms
from .models import Instituicao, UnidadeAdministrativa


class InstituicaoForm(forms.ModelForm):
    class Meta:
        model = Instituicao
        fields = ['nome', 'sigla', 'cor_tema']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'block w-full h-12 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-600 sm:text-sm text-gray-900',
                'placeholder': 'Nome da instituição'
            }),
            'sigla': forms.TextInput(attrs={
                'class': 'block w-full h-12 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-600 sm:text-sm text-gray-900',
                'placeholder': 'Ex: MEC, MS, TCU'
            }),
            'cor_tema': forms.TextInput(attrs={
                'class': 'block w-full h-12 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-600 sm:text-sm text-gray-900',
                'type': 'color',
                'placeholder': '#3B82F6'
            }),
        }


class UnidadeAdministrativaForm(forms.ModelForm):
    class Meta:
        model = UnidadeAdministrativa
        fields = ['nome', 'instituicao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'block w-full h-12 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-600 sm:text-sm text-gray-900',
                'placeholder': 'Nome da unidade administrativa'
            }),
            'instituicao': forms.Select(attrs={
                'class': 'block w-full h-12 border border-gray-300 bg-gray-50 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-600 sm:text-sm text-gray-900'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        # Extrai instituição ativa se fornecida
        instituicao_ativa = kwargs.pop('instituicao_ativa', None)
        super().__init__(*args, **kwargs)
        
        # Se há uma instituição ativa, oculta o campo instituição
        if instituicao_ativa:
            self.fields['instituicao'].widget = forms.HiddenInput()
            self.fields['instituicao'].initial = instituicao_ativa