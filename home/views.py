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
        
        # Se há uma instituição ativa, filtra os dados por ela
        if hasattr(self.request, 'instituicao_ativa'):
            instituicao_ativa = self.request.instituicao_ativa
            context['unidades_count'] = UnidadeAdministrativa.objects.filter(instituicao=instituicao_ativa).count()
            context['pdtics_count'] = PDTIC.objects.filter(instituicao=instituicao_ativa).count()
            # No contexto de uma instituição específica, não mostra contagem total de instituições
            context['instituicoes_count'] = 1  # A própria instituição ativa
        else:
            # Modo global (sem instituição ativa)
            context['instituicoes_count'] = Instituicao.objects.count()
            context['unidades_count'] = UnidadeAdministrativa.objects.count()
            context['pdtics_count'] = PDTIC.objects.count()
            
        return context
