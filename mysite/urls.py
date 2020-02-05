from django.urls import path
from .views import MarketList, ProductDetail, DetailCategory, add_item, cart_list, form_order, checkout, delete_item, filter_shop
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('category/filter', filter_shop, name='filter'),
    path('delete_item', delete_item, name='delete_item'),
    path('category/add_item', add_item, name='add_item'),
    path('product/<slug:slug>', ProductDetail.as_view(), name='detail'),
    path('', MarketList.as_view(), name='home'),
    path('cart_all', cart_list, name='cart_all'),
    path('cart_all/form_order', form_order, name='form_order'),
    path('checkout', checkout, name='checkout'),
    path('category/<slug:slug>', DetailCategory.as_view(), name='category'),
] 
