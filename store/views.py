from django.http import HttpResponse
from django.shortcuts import render

from store.models import Product, Category, Cart, CartItem


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
        return render(request, '404.html')

    return render(request, 'product.html', context={'product': prod})


def cart(request):

    # pseudo data without querying db about cart. products are from db.
    c = Cart(created="2024-10-20", updated="2024-10-21")
    prod1 = Product.objects.filter(title="Rqawiteli").first()
    prod2 = Product.objects.filter(title="Mwvane Vashli").first()
    print(prod2)
    item1 = CartItem(product=prod1, quantity=100)
    item1 = {"item": item1, "total": item1.quantity * item1.product.price}
    item2 = CartItem(product=prod2, quantity=200)
    item2 = {"item": item2, "total": item2.quantity * item2.product.price}

    return render(request, 'cart.html', context={'cart': c,
                                                 'items': [item1, item2]})


def checkout(request):
    return render(request, 'checkout.html')


def contact(request):
    return render(request, 'contact.html')
