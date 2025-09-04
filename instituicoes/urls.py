from django.urls import path
from .views import *

urlpatterns = [
    # URLs Instituição
    path('', InstituicaoList.as_view(), name='instituicao_list'),
    path('<int:pk>/', InstituicaoDetail.as_view(), name='instituicao_detail'),
    path('novo/', InstituicaoCreate.as_view(), name='instituicao_create'),
    path('<int:pk>/editar/', InstituicaoUpdate.as_view(), name='instituicao_update'),
    path('<int:pk>/excluir/', InstituicaoDelete.as_view(), name='instituicao_delete'),

    # Unidades Administrativas por Instituição
    path('<int:instituicao_pk>/unidades/', UnidadeList.as_view(), name='instituicao_unidades'),
    path('unidades/', UnidadeList.as_view(), name='unidade_list'),
    path('unidades/novo/', UnidadeCreate.as_view(), name='unidade_create'),
    path('unidades/<int:pk>/editar/', UnidadeUpdate.as_view(), name='unidade_update'),
    path('unidades/<int:pk>/excluir/', UnidadeDelete.as_view(), name='unidade_delete'),
]