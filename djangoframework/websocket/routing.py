from django.urls import re_path
from .consumers.consumers import BackgroundTaskConsumer
from websocket.consumers import basic_consumers


websocket_urlpatterns = [
    re_path(r'ws/background-task/$', BackgroundTaskConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', basic_consumers.ChatConsumer.as_asgi()),
    
]