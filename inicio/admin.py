from django.contrib import admin
from django.contrib.admin.decorators import register
from . models import Product

@register(Product)
class ProductS(admin.ModelAdmin):
    list_display = ['nome','preco']