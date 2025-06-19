
from django.urls import path
from .consumers import OrderConsumer

websocket_urlpatterns = [
    path('ws/order-notify/', OrderConsumer.as_asgi()),
]

