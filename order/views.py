from django.db.models import F, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View


from order.models import CartItem, Cart
from store.models import Product
import store.views

# Create your views here.
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


class AddToCartView(View):
    def post(self, request, slug=None):
        product_title = request.POST.get('add')
        prod = Product.objects.filter(title=product_title).first()
        cart = Cart.objects.prefetch_related('items').get_or_create(id=1)[0]

        for cart_item in cart.items.all():
            if cart_item.product.title == product_title:
                cart_item.quantity += 1
                cart_item.save()
                return redirect('cart')

        cart_item = CartItem.objects.create(cart=cart, product=prod, quantity=prod.min_weight)
        cart_item.save()

        return redirect('cart')

