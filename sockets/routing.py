from django.urls import re_path
from . import consumers
from notifications import consumers as notif_consumers
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
            re_path(r'ws/notifications/(?P<username>\w+)/$', notif_consumers.Notifications.as_asgi()),
        ])
    ),
})