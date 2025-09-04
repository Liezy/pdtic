from django.urls import path
from . import views

urlpatterns = [
    path("", views.pdtic_list, name="pdtic_list"),
    path("instituicao/<int:instituicao_pk>/", views.pdtic_list_by_instituicao, name="instituicao_pdtics"),
    path("<int:pk>/", views.pdtic_detail, name="pdtic_detail"),
    path("novo/", views.pdtic_create, name="pdtic_create"),
]
