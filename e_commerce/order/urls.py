from django.urls import path
from .views import OrderCreateView, OrderStatusUpdateView,CartItemView

urlpatterns = [
    path('orders/', OrderCreateView.as_view(), name='create-order'),
    path('cart/', CartItemView.as_view(), name='cart'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='update-order-status'),
]
