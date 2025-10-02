from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from datetime import datetime, timedelta

class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from instituicoes.models import Instituicao, UnidadeAdministrativa
        from pdtic.models import PDTIC
        
        # Se há uma instituição ativa, mostra dashboard específico da instituição
        if hasattr(self.request, 'instituicao_ativa'):
            instituicao_ativa = self.request.instituicao_ativa
            context['title'] = f'Dashboard - {instituicao_ativa.nome}'
            context['is_instituicao_dashboard'] = True
            
            # Métricas da instituição
            context['unidades_count'] = UnidadeAdministrativa.objects.filter(instituicao=instituicao_ativa).count()
            context['pdtics_count'] = PDTIC.objects.filter(instituicao=instituicao_ativa).count()
            
            # PDTICs por status
            pdtics_qs = PDTIC.objects.filter(instituicao=instituicao_ativa)
            context['pdtics_aprovados'] = pdtics_qs.filter(status='aprovado').count()
            context['pdtics_publicados'] = pdtics_qs.filter(status='publicado').count()
            context['pdtics_elaboracao'] = pdtics_qs.filter(status='elaboracao').count()
            context['pdtics_rascunho'] = pdtics_qs.filter(status='rascunho').count()
            
            # PDTICs recentes (último mês)
            um_mes_atras = datetime.now() - timedelta(days=30)
            context['pdtics_recentes'] = pdtics_qs.filter(criado_em__gte=um_mes_atras).count()
            
            # Lista dos últimos PDTICs criados
            context['ultimos_pdtics'] = pdtics_qs.order_by('-criado_em')[:5]
            
            # Estatísticas das unidades (todas as unidades da instituição)
            unidades_com_pdtic = 0  # Como PDTIC não tem relação direta com unidade, vamos deixar como 0 por enquanto
            
            context['unidades_com_pdtic'] = unidades_com_pdtic
            context['unidades_sem_pdtic'] = context['unidades_count'] - unidades_com_pdtic
            
        else:
            # Modo administrativo global (sem instituição ativa)
            context['title'] = 'Painel Administrativo - Sistema PDTIC'
            context['is_instituicao_dashboard'] = False
            
            # Métricas globais para administradores
            context['instituicoes_count'] = Instituicao.objects.count()
            context['unidades_count'] = UnidadeAdministrativa.objects.count()
            context['pdtics_count'] = PDTIC.objects.count()
            
            # Instituições mais ativas (com mais PDTICs)
            context['instituicoes_ativas'] = Instituicao.objects.annotate(
                total_pdtics=Count('planos')
            ).order_by('-total_pdtics')[:5]
            
        return context
