from django.contrib import admin
from .models import Product, Category,Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    search_fields = ('name',)
    list_filter = ('category',)
    list_editable = ('price', 'stock')

admin.site.register(Category)
admin.site.register(Order)

