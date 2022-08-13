from django.contrib import admin
from .models import Products, orderDetail

# Register your models here.

admin.site.site_header = 'Buy & Sell Website'
admin.site.site_title = 'buyNsell'
admin.site.index_title = 'Manage buyNsell'

class ProductsAdmin(admin.ModelAdmin):
    list_display  = ('name', 'price', 'desc')
    search_fields = ('name',)

    def discount_100(self, request, queryset):
        queryset.update(price=0)
    
    actions = ('discount_100',)

    list_editable = ('price', 'desc')
admin.site.register(Products, ProductsAdmin)
admin.site.register(orderDetail)
