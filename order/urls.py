from django.urls import path
from order.views import CartView, CheckoutView, AddToCartView

urlpatterns = [
    path('order/cart/', CartView.as_view(), name='cart'),
    path('order/checkout', CheckoutView.as_view(), name='checkout'),
    path('order/add_to_cart', AddToCartView.as_view(), name='add_to_cart'),
]
