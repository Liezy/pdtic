def instituicao_context(request):
    """
    Context processor para disponibilizar dados da instituição ativa
    """
    context = {}
    
    # Verifica se existe uma instituição ativa
    if hasattr(request, 'instituicao_ativa'):
        context['instituicao_ativa'] = request.instituicao_ativa
        # Disponibiliza a cor tema para facilitar o uso nos templates
        context['cor_tema'] = request.instituicao_ativa.cor_tema
    else:
        context['instituicao_ativa'] = None
        context['cor_tema'] = '#3B82F6'  # Cor padrão
    
    return context