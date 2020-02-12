from django.contrib import admin
from .models import *

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

@admin.register(StatusOrder)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_price', 'fullname', 'user', 'email', 'phone', 'city', 'status', 'created', )
    list_filter = ['created']
    inlines = [OrderItemInline]


class SizeFeatureAdmin(admin.TabularInline):
    model = SizeFeature
    raw_id_field = ['product']
 
class ColorFeatureAdmin(admin.TabularInline):
    model = ColorFeature
    raw_id_field = ['product']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [SizeFeatureAdmin]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [ColorFeatureAdmin]
 
 
 