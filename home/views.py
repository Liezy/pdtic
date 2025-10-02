from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views import View
from datetime import datetime, timedelta
import json

class LandingPageView(TemplateView):
    template_name = 'home/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context

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


class CalendarEventsView(View):
    """View para fornecer eventos para o FullCalendar"""
    
    def get(self, request, *args, **kwargs):
        from pdtic.models import PDTIC
        
        # Pega parâmetros de data do FullCalendar
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')
        
        # Filtra eventos baseado na instituição ativa
        if hasattr(request, 'instituicao_ativa') and request.instituicao_ativa:
            pdtics = PDTIC.objects.filter(instituicao=request.instituicao_ativa)
        else:
            # Modo admin - mostra todos os PDTICs
            pdtics = PDTIC.objects.all()
        
        # Se temos datas de filtro, aplicamos
        if start_date and end_date:
            try:
                start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                # Filtra PDTICs criados no período
                pdtics = pdtics.filter(criado_em__date__range=[start.date(), end.date()])
            except ValueError:
                pass  # Se formato de data inválido, ignora filtro
        
        # Converte PDTICs para formato de eventos do FullCalendar
        events = []
        for pdtic in pdtics:
            # Cor do evento baseada no status
            color_map = {
                'rascunho': '#6B7280',      # Cinza
                'elaboracao': '#F59E0B',    # Amarelo
                'aprovado': '#10B981',      # Verde
                'publicado': '#3B82F6',     # Azul
            }
            
            event = {
                'id': str(pdtic.id),
                'title': pdtic.titulo[:50] + ('...' if len(pdtic.titulo) > 50 else ''),
                'start': pdtic.criado_em.isoformat(),
                'color': color_map.get(pdtic.status, '#6B7280'),
                'extendedProps': {
                    'status': pdtic.get_status_display(),
                    'instituicao': pdtic.instituicao.nome if pdtic.instituicao else 'N/A',
                    'description': f"Status: {pdtic.get_status_display()}\nInstituição: {pdtic.instituicao.nome if pdtic.instituicao else 'N/A'}"
                }
            }
            
            # Adiciona datas de vencimento se existirem (exemplo de datas fictícias)
            # Você pode adicionar campos de data no modelo PDTIC conforme necessário
            if pdtic.status in ['elaboracao', 'aprovado']:
                # Adiciona um evento de prazo 30 dias após criação (exemplo)
                prazo_date = pdtic.criado_em + timedelta(days=30)
                prazo_event = {
                    'id': f'prazo_{pdtic.id}',
                    'title': f'Prazo: {pdtic.titulo[:30]}...',
                    'start': prazo_date.isoformat(),
                    'color': '#EF4444',  # Vermelho para prazos
                    'extendedProps': {
                        'type': 'prazo',
                        'status': 'Prazo de Conclusão',
                        'instituicao': pdtic.instituicao.nome if pdtic.instituicao else 'N/A',
                        'description': f"Prazo de conclusão do PDTIC\n{pdtic.titulo}"
                    }
                }
                events.append(prazo_event)
            
            events.append(event)
        
        return JsonResponse(events, safe=False)
