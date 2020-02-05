from decimal import Decimal
from django.conf import settings
from mysite.models import Product


class Cart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {} 
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity,
                                     'price': int(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product_id]['quantity'] += int(quantity)
        self.cart[product_id]['total'] = self.cart[product_id]['quantity'] * self.cart[product_id]['price']
        self.save()

    # Сохранение данных в сессию
    def save(self):  
        self.session[settings.CART_SESSION_ID].update(self.cart) 
        # Указываем, что сессия изменена
        self.session.modified = True

    def remove(self, product_id):  
        if str(product_id) in self.cart:  
            del self.cart[str(product_id)]  
            self.save()

    def __iter__(self): 
        for key, value in self.cart.items():
            products = Product.objects.filter(id=key)
            for product in products:
                self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = item['price'] 
            yield item

    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
