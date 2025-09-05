from django.urls import path
from . import views

urlpatterns = [
    path("", views.pdtic_list, name="pdtic_list"),
    path("instituicao/<int:instituicao_pk>/", views.pdtic_list_by_instituicao, name="instituicao_pdtics"),
    path("<int:pk>/", views.pdtic_detail, name="pdtic_detail"),
    path("novo/", views.pdtic_create, name="pdtic_create"),
    path("<int:pk>/editar/", views.pdtic_update, name="pdtic_update"),
    
    # URLs para versões
    path("<int:pdtic_pk>/versoes/", views.versao_list, name="versao_list"),
    path("<int:pdtic_pk>/versoes/nova/", views.versao_create, name="versao_create"),
    path("<int:pdtic_pk>/versoes/<int:pk>/", views.versao_detail, name="versao_detail"),
    path("<int:pdtic_pk>/versoes/<int:pk>/editar/", views.versao_update, name="versao_update"),
    path("<int:pdtic_pk>/versoes/<int:pk>/excluir/", views.versao_delete, name="versao_delete"),
]
