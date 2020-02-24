from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('search/', SearchField.as_view(), name='search'),

    path('category/filter', Filter.as_view(), name='filter'),
    path('delete_item/', DeleteItem.as_view(), name='delete_item'),
    path('category/add_item', AddItem.as_view(), name='add_item'),
    path('product/<slug:slug>', ProductDetail.as_view(), name='detail'),    
    path('', MarketList.as_view(), name='home'),
    path('category/<slug:slug>', DetailCategory.as_view(), name='category'),
   
    path('cart_all', CartList.as_view(), name='cart_all'),
    path('cart_all/form_order', Order.as_view(), name='form_order'),
    path('checkout', Checkout.as_view(), name='checkout'),
] 
