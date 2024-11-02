from django.urls import path
from store.views import IndexView, CategoryView, ProductView, ContactView, RegisterView, Logout, LoginView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('category/', CategoryView.as_view(), name='category'),
    path('product/<slug:slug>/', ProductView.as_view(), name='product'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]