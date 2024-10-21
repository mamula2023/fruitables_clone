from django.urls import path
from store import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('product/<slug:slug>/', views.product, name='product'),
    path('order/cart/', views.cart, name='cart'),
    path('order/checkout', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
]