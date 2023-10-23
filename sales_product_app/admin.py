from django.contrib import admin
from .models import Product, Category, Shop, CustomUser

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(CustomUser)
# Register your models here.
