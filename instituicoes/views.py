from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Instituicao, UnidadeAdministrativa

# --- Instituição ---
class InstituicaoList(ListView):
    model = Instituicao

class InstituicaoDetail(DetailView):
    model = Instituicao
    template_name = 'instituicoes/instituicao_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instituicao = self.get_object()
        context['unidades_count'] = instituicao.unidades.count()
        context['pdtics_count'] = instituicao.planos.count()
        return context

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
    template_name = 'unidades/unidade_list.html'
    
    def get_queryset(self):
        # Se vier de uma instituição específica, filtra por ela
        if 'instituicao_pk' in self.kwargs:
            return self.model.objects.filter(instituicao_id=self.kwargs['instituicao_pk'])
        return self.model.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Se vier de uma instituição específica, adiciona ela ao contexto
        if 'instituicao_pk' in self.kwargs:
            context['instituicao'] = Instituicao.objects.get(pk=self.kwargs['instituicao_pk'])
        return context

class UnidadeCreate(CreateView):
    model = UnidadeAdministrativa
    fields = ['nome', 'instituicao']
    template_name = 'unidades/unidade_form.html'
    success_url = reverse_lazy('unidade_list')

class UnidadeUpdate(UpdateView):
    model = UnidadeAdministrativa
    fields = ['nome', 'instituicao']
    template_name = 'unidades/unidade_form.html'
    success_url = reverse_lazy('unidade_list')

class UnidadeDelete(DeleteView):
    model = UnidadeAdministrativa
    template_name = 'unidades/unidade_confirm_delete.html'
    success_url = reverse_lazy('unidade_list')
