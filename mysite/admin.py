from django.contrib import admin
from .models import Category, Product, Gallery, Order, OrderItem, Feature, Size, ColorFeature

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):  
    list_display = ('name', 'parent', )


class GalleryAdmin(admin.TabularInline):
    model = Gallery
    raw_id_field = ['product']
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [GalleryAdmin]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'user', 'email', 'city', 'created', )
    list_filter = ['created']
    inlines = [OrderItemInline]

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', )

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(ColorFeature)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', )
