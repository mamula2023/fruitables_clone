from django.http import HttpResponse
from django.shortcuts import render

from store.models import Product, Category


# Create your views here.
def index(request):
    return render(request, 'index.html')


def category(request, slug):
    cat = Category.objects.prefetch_related('products').filter(title=slug).first()
    products = cat.products.all()
    return render(request, 'category.html', {'category': cat, "products": products})


def product(request, slug):
    prod = Product.objects.filter(title=slug).first()
    if prod is None:
        print("hello world")
        return render(request, '404.html')
    return render(request, 'product.html', context={'product': prod})


def cart(request):
    return HttpResponse("Hello, world. You're at the polls cart.")


def checkout(request):
    return HttpResponse("Hello, world. You're at the polls checkout.")


def contact(request):
    return render(request, 'contact.html')
