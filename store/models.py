from django.db import models


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='static/img/', default='default.jpg')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    origin = models.CharField(max_length=100)
    quality = models.CharField(max_length=100)
    check_attr = models.BooleanField(default=False)
    min_weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=1)
