from django.urls import path
from . import views as sockets_views

urlpatterns = [
    path('', sockets_views.index, name='private-message'),
    path('<str:room_name>/', sockets_views.room, name='room'),
]