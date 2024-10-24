from django.contrib import admin

from store.models import Product, Category, Tag, CartItem, Cart

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Cart)
admin.site.register(CartItem)
