from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from store.models import Product, Category, Cart, CartItem, Tag


class IndexView(View):
    def get(self, request):
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


class CategoryView(View):
    def get(self, request, slug=None):
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
        paginator = Paginator(products, 3)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context['paginator'] = page_obj
        context['tags'] = tags

        cart, created = Cart.objects.prefetch_related('items').get_or_create(id=1)
        context['items_in_cart'] = len(list(cart.items.all())) if not created else 0

        return render(request, 'category.html', context)

    def post(self, request, slug=None):
        add_to_cart(request)
        return self.get(request, slug)


class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CartView(View):
    template_name = 'cart.html'

    def get(self, request):
        cart = get_object_or_404(Cart.objects.prefetch_related('items'), id=1)
        items = cart.items.all().annotate(total=F('quantity') * F('product__price'))
        subtotal = items.aggregate(subtotal=Sum('total'))

        if subtotal['subtotal'] is None:
            subtotal['subtotal'] = 0

        context = {
            'items': items,
            'subtotal': subtotal.get('subtotal')
        }
        return render(request, self.template_name, context)

    def post(self, request):
        remove = request.POST.get('remove')
        increase = request.POST.get('increase')
        decrease = request.POST.get('decrease')

        if remove is not None:
            CartItem.objects.filter(id=remove).delete()
        elif increase is not None:
            obj = get_object_or_404(CartItem, id=increase)
            obj.quantity += 1
            obj.save()
        elif decrease is not None:
            obj = get_object_or_404(CartItem, id=decrease)
            if obj.quantity > 1:
                obj.quantity -= 1
                obj.save()
            else:
                obj.delete()
        return self.get(request)


class CheckoutView(View):
    def get(self, request):
        return render(request, 'checkout.html')


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')
