from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
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




class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """Creates and returns a user with a username and password."""
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """Creates and returns a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    last_active_datetime = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()

    def update_last_active(self):
        self.last_active_datetime = timezone.now()
        self.save(update_fields=['last_active_datetime'])
