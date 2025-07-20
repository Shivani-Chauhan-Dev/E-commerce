from django.urls import path
from .consumers import OrderStatusConsumer

websocket_urlpatterns = [
    path("ws/orders/", OrderStatusConsumer.as_asgi()),
]
