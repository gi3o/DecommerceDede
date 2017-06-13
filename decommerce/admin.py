from django.contrib import admin
from .models import *

# Register your models here.

class DecadeBornListFilter(admin.SimpleListFilter):
    title = 'Price'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('0', '< 10'),
            ('10', '>= 10'),
            ('50', '>= 50'),
            ('100', '>= 100'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(price__lt=10)
        if self.value() == '10':
            return queryset.filter(price__gte=10)
        if self.value() == '50':
            return queryset.filter(price__gte=50)
        if self.value() == '100':
            return queryset.filter(price__gte=100)

class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Product Info', {'fields':['name', 'price', 'category', 'image']}),
        ('Details', {'fields':['details', 'seller', 'stock'], 'classes':['collapse']}),
    ]
    list_display = ('name', 'category', 'seller', 'price')
    list_filter = [DecadeBornListFilter, 'seller']
    search_fields = ['name']

admin.site.register(Product, ProductAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info', {'fields':['user', 'nationality', 'address', 'cart']})
    ]
    list_display = ['user', 'nationality', 'address']
    list_filter = ['nationality']
    search_fields = ['user']

admin.site.register(UserProfile, UserProfileAdmin)

class SellerProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Store Name', {'fields':['user', 'store_name']})
    ]
    list_display = ['user', 'store_name']
    search_fields = ['user']

admin.site.register(SellerProfile, SellerProfileAdmin)

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)

class SellerReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info', {'fields':['seller', 'by']}),
        ('Review', {'fields':['stars', 'review'], 'classes':['collapse']}),
    ]
    list_display = ['by', 'seller', 'stars']
    list_filter = ['stars', 'by']
    search_fields = ['by', 'seller']

admin.site.register(SellerReview, SellerReviewAdmin)

class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info', {'fields':['product', 'user', 'quantity']}),
    ]
    list_display = ['product', 'user', 'quantity']
    search_fields = ['product', 'user']

admin.site.register(Order, OrderAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info', {'fields':['product', 'by']}),
        ('Review', {'fields':['title', 'stars', 'review'], 'classes':['collapse']}),
    ]
    list_display = ['by', 'product', 'stars']
    list_filter = ['stars', 'by']
    search_fields = ['by', 'product']

admin.site.register(ProductReview, ProductReviewAdmin)

admin.site.register(CartItem)
