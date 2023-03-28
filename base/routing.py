from django.urls import path
from base.consumers import BaseConsumer

websocket_urlpatterns = [
    path("" , BaseConsumer.as_asgi()) , 
]