from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Instituicao, UnidadeAdministrativa

# --- Instituição ---
class InstituicaoList(ListView):
    model = Instituicao

class InstituicaoCreate(CreateView):
    model = Instituicao
    fields = ['nome', 'sigla']
    success_url = reverse_lazy('instituicao_list')

class InstituicaoUpdate(UpdateView):
    model = Instituicao
    fields = ['nome', 'sigla']
    success_url = reverse_lazy('instituicao_list')

class InstituicaoDelete(DeleteView):
    model = Instituicao
    success_url = reverse_lazy('instituicao_list')


# --- Unidade Administrativa ---
class UnidadeList(ListView):
    model = UnidadeAdministrativa

class UnidadeCreate(CreateView):
    model = UnidadeAdministrativa
    fields = ['nome', 'instituicao']
    success_url = reverse_lazy('unidade_list')

class UnidadeUpdate(UpdateView):
    model = UnidadeAdministrativa
    fields = ['nome', 'instituicao']
    success_url = reverse_lazy('unidade_list')

class UnidadeDelete(DeleteView):
    model = UnidadeAdministrativa
    success_url = reverse_lazy('unidade_list')
