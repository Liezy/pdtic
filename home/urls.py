from django.urls import path
from .views import HomeView, LandingPageView, CalendarEventsView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('dashboard/', HomeView.as_view(), name='home'),
    path('api/calendar-events/', CalendarEventsView.as_view(), name='calendar_events'),
]
