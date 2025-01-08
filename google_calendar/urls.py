# calendar_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.get_events, name='get_events'),
    path('create_event/', views.create_event, name='create_event'),
]
