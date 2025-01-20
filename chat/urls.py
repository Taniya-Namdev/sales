from django.urls import path 
from .views import *

urlpatterns = [
    path('',Index.as_view(),name='index'),
    path('home/', ChatHome.as_view(), name='chat_home'),
    path('<str:room_name>/',Room.as_view(),name='room'),
]
