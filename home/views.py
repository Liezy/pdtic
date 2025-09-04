from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sistema PDTIC'
        from instituicoes.models import Instituicao, UnidadeAdministrativa
        from pdtic.models import PDTIC
        context['instituicoes_count'] = Instituicao.objects.count()
        context['unidades_count'] = UnidadeAdministrativa.objects.count()
        context['pdtics_count'] = PDTIC.objects.count()
        return context
