from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from store.models import Product, Category, Cart, CartItem, Tag


# Create your views here.
def index(request):
    return render(request, 'index.html')

def add_to_cart(request):
    product_title = request.POST.get('add')
    prod = Product.objects.filter(title=product_title).first()

    cart = Cart.objects.prefetch_related('items').get_or_create(id=1)[0]

    for cart_item in cart.items.all():
        if cart_item.product.title == product_title:
            cart_item.quantity += 1
            cart_item.save()
            return

    cart_item = CartItem.objects.create(cart=cart, product=prod, quantity=prod.min_weight)
    cart_item.save()





def category(request, slug=None):
    if request.method == 'POST':
        add_to_cart(request)

    tag = request.GET.get('tag')
    price = request.GET.get('rangeInput')
    if price is None or int(price) == 0:
        price = 999999999

    context = {'child_categories': [], 'paginator': None, 'tags': [], 'category': ""}
    products = []
    if slug is None:
        cats = Category.objects.prefetch_related('parent')
        products = Product.objects.prefetch_related('tags').filter(price__lte=price).all()

        result = []

        if tag is not None:
            for prod in products:
                tags = prod.tags.all()
                for t in tags:
                    if t.title == tag:
                        result.append(prod)

            products = result

        children = cats.filter(parent_category_id=None).all()
        context['child_categories'] = children

    else:
        cats = Category.objects.prefetch_related('products', 'parent')
        parent_cat = cats.get(title=slug)
        context['category'] = parent_cat.title

        cat_id = parent_cat.id
        children = cats.filter(parent_category_id=cat_id)
        context['child_categories'] = children
        cats_queue = [slug]

        for prod in parent_cat.products.filter(price__lte=price).all():
            products.append(prod)

        while len(cats_queue) > 0:
            cat = cats_queue.pop(0)
            cat_id = cats.filter(title=cat).first().id
            children = cats.filter(parent_category_id=cat_id)

            for child in children:
                prods = child.products.filter(price__lte=price).all()
                for prod in prods:
                    if prod not in products:
                        products.append(prod)

                cats_queue.append(child.title)

    tags = Tag.objects.all()

    paginator = Paginator(products, 10)

    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    context['paginator'] = page_obj
    context['tags'] = tags

    return render(request, 'category.html', context)


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
