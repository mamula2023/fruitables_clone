from django.db import models
from django.utils.text import slugify
from versatileimagefield.fields import VersatileImageField


# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = VersatileImageField('Image', upload_to='static/img/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField('Tag', related_name='products', blank=True)
    origin = models.CharField(max_length=100)
    quality = models.CharField(max_length=100)
    check_attr = models.BooleanField(default=False)
    min_weight = models.DecimalField(max_digits=7, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, default="category")
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE,
                                        null=True, blank=True, related_name='parent')

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True, default="tag")

    def __str__(self):
        return self.title


