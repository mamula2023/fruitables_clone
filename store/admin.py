from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from store.models import Product, Category, Tag, CustomUser

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'last_active_datetime', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('last_active_datetime',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('last_active_datetime',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
