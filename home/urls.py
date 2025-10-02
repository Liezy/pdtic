from django.urls import path
from .views import HomeView, LandingPageView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('dashboard/', HomeView.as_view(), name='home'),
]
