from django.contrib import admin
from .models import Instituicao, UnidadeAdministrativa

@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sigla', 'cor_tema')
    search_fields = ('nome', 'sigla')
    fields = ('nome', 'sigla', 'cor_tema')

@admin.register(UnidadeAdministrativa)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'instituicao')
    search_fields = ('nome',)
    list_filter = ('instituicao',)
