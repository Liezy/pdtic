from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from instituicoes.models import Instituicao


class InstituicaoMiddleware:
    """
    Middleware para controlar qual instituição está ativa na sessão
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs que não precisam de instituição selecionada
        self.exempt_urls = [
            '/admin/',
            '/selecionar-instituicao/',
            '/ativar-instituicao/',
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        # Verifica se a URL está isenta da verificação
        path = request.path
        if any(path.startswith(url) for url in self.exempt_urls):
            response = self.get_response(request)
            return response

        # Verifica se existe uma instituição ativa na sessão
        instituicao_id = request.session.get('instituicao_ativa')
        
        if instituicao_id:
            try:
                # Verifica se a instituição ainda existe
                instituicao = Instituicao.objects.get(id=instituicao_id)
                # Adiciona a instituição ao request para fácil acesso
                request.instituicao_ativa = instituicao
            except Instituicao.DoesNotExist:
                # Remove instituição inválida da sessão
                del request.session['instituicao_ativa']
                return redirect('selecionar_instituicao')
        else:
            # Redireciona para seleção de instituição se não houver uma ativa
            if path != reverse('selecionar_instituicao'):
                return redirect('selecionar_instituicao')

        response = self.get_response(request)
        return response