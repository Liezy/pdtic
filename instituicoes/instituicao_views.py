from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse
from django.urls import reverse
from .models import Instituicao


class SelecionarInstituicaoView(ListView):
    """
    View para exibir lista de instituições e permitir seleção
    """
    model = Instituicao
    template_name = 'instituicoes/selecionar_instituicao.html'
    context_object_name = 'instituicoes'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Selecione uma Instituição'
        return context


def ativar_instituicao(request, instituicao_id):
    """
    View para ativar uma instituição específica na sessão
    """
    # Só aceita requisições POST
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)
    
    instituicao = get_object_or_404(Instituicao, id=instituicao_id)
    
    # Salva a instituição ativa na sessão
    request.session['instituicao_ativa'] = instituicao.id
    
    # Sempre retorna JSON para requisições AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'redirect_url': reverse('home'),
            'instituicao_nome': instituicao.nome
        })
    
    # Redireciona para o dashboard da instituição (fallback)
    return redirect('home')


def trocar_instituicao(request):
    """
    View para trocar de instituição (limpa a sessão e volta para seleção)
    """
    if 'instituicao_ativa' in request.session:
        del request.session['instituicao_ativa']
    
    return redirect('selecionar_instituicao')