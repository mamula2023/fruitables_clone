from django.urls import path
from store import views
from store.views import IndexView, CategoryView, ProductView, CartView, CheckoutView, ContactView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('category/', CategoryView.as_view(), name='category'),
    path('product/<slug:slug>/', ProductView.as_view(), name='product'),
    path('order/cart/', CartView.as_view(), name='cart'),
    path('order/checkout', CheckoutView.as_view(), name='checkout'),
    path('contact/', ContactView.as_view(), name='contact'),
]