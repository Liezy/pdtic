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
            '/trocar-instituicao/',
            '/static/',
            '/media/',
        ]
        # URLs que são APENAS para modo administrativo (sem instituição ativa)
        self.admin_only_paths = [
            '/instituicoes/',  # Lista de instituições é só para admins
        ]
        # URLs que devem ser permitidas mesmo com instituição ativa
        self.allowed_with_institution = [
            '/instituicoes/unidades/',
            '/pdtic/',
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
                
                # Se há instituição ativa mas está tentando acessar URL administrativa,
                # redireciona para o dashboard da instituição
                # EXCETO se for uma URL permitida com instituição ativa
                if any(path.startswith(url) for url in self.admin_only_paths):
                    # Permite acesso se for uma URL específica permitida
                    if not any(path.startswith(url) for url in self.allowed_with_institution):
                        return redirect('home')
                    
            except Instituicao.DoesNotExist:
                # Remove instituição inválida da sessão
                del request.session['instituicao_ativa']
                return redirect('selecionar_instituicao')
        else:
            # Redireciona para seleção de instituição se não houver uma ativa
            # EXCETO se for para páginas administrativas (nesse caso permite acesso)
            if not any(path.startswith(url) for url in self.admin_only_paths):
                if path != reverse('selecionar_instituicao'):
                    return redirect('selecionar_instituicao')

        response = self.get_response(request)
        return response