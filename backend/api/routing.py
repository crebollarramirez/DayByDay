from django.urls import re_path
from .consumers import ChatBotConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', ChatBotConsumer.as_asgi()),  # Ensure this matches
]