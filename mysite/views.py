from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, ListView, DetailView, CreateView
from .models import *
from django.conf import settings
from .cart import Cart
from .forms import Form_Order
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO 
from django.db.models import Max, Min, Q
from django.contrib.auth.models import User
from django.views import View
from django.contrib.postgres.search import SearchVector


class MarketList(ListView):

    model = Category
 
    template = 'category_list.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Category.objects.filter(parent__isnull=True)
        products = Product.objects.parents_isnull()
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            products_all = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            products_all = paginator.page(1)
        except EmptyPage:
            products_all = paginator.page(paginator.num_pages)

        context['categories'] = data
        context['products'] = products_all
        context['page'] = page
        context['title'] = "Список товаров"
        return context


class DetailCategory(DetailView):

    model = Category
    template = 'mysite/category_detail.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Category.objects.filter(parent__isnull=True)
        products = Product.objects.is_active().get_parent(self.get_object()).order_by('price')
        
        cart = Cart(self.request)
        page = self.request.GET.get('page')
        
        paginator = Paginator(products, self.paginate_by)
        
        size = Size.objects.all()
        color = Color.objects.all()

        try:
            products_all = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            products_all = paginator.page(1)
        except EmptyPage:
            products_all = paginator.page(paginator.num_pages)
 
        context['cart'] = len(cart)
        context['categories'] = data
        context['products'] = products_all
        context['count'] = products.count()
        context['max'] = products.aggregate(Max('price'))
        context['min'] = products.aggregate(Min('price'))
        context['page'] = page
        context['size'] = size
        context['color'] = color
        context['category'] = self.get_object()
        
        context['title'] = "Список товаров"
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'mysite/detail.html'

    def get_context_data(self, **kwargs):
        product = self.get_object() 
        context = super().get_context_data(**kwargs)
        context['instance'] = product
        context['title'] = str(product)
        return context


class AddItem(View):

    def get(self, request, *args, **kwargs): 
        quantity = request.GET.get('quantity')
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        cart = Cart(request)  
        cart.add(product, quantity, True)
        data = Category.objects.filter(parent__isnull=True)
        products = Product.objects.get_parent(product.parent).order_by('price')
        page = request.GET.get('page')
        if page == None:
            page = 1
        try:
            paginator = Paginator(products, 6)
            products_all = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            products_all = paginator.page(1)
        except EmptyPage:
            products_all = paginator.page(paginator.num_pages)
   

        content = {
            'cart': len(cart), 
            'categories': data,
            'products': products_all,
            'count': products.count(),
            'title': "Список товаров",
            'page': page 
        }
        return render(request, "mysite/category_detail.html", content)


class DeleteItem(View):

    def get(self,  request, *args, **kwargs):
        cart = Cart(request) 
        product_id = request.GET.get('product_id')
        # product = Product.objects.get(id=product_id)
        cart.remove(product_id) 
        content = {
            'cart': len(cart),
            'cart_all': cart,
            'title': "Ваша корзина"
        }
        return render(request, "mysite/cart_list.html", content)

class CartList(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        content = {
            'cart': len(cart),
            'cart_all': cart,
            'title': "Ваша корзина"
        }
        print(cart.cart)
        return render(request, "mysite/cart_list.html", content)


class Filter(View):

    def get(self, request, *args, **kwargs):
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        size_arr = request.GET.getlist('size[]')
        color_arr = request.GET.getlist('color[]')  
          
        color_filter = ColorFeature.objects.filter(color__in=list(Color.objects.filter(name__in=color_arr) ))
        product_f = set()
        for it in color_filter:
            product_f.add(str(it.product))  
        name_category = request.GET.get('category') 
        parent = Category.objects.get(name=name_category) 
        product_f = list(product_f)
        products = Product.objects.is_active().get_parent(parent) 
        if not len(product_f) == 0:
            products = products.name_in(product_f) 
        if not price_from == 0: 
            products = products.prices_gte(price_from)
        if not price_to == 0: 
            products = products.price_lte(price_to)
        
        page = request.GET.get('page') 
        paginator = Paginator(products, 6)
        
        size = Size.objects.all()
        color = Color.objects.all()

        data = Category.objects.filter(parent__isnull=True) 
        
        cart = Cart(request)

        try:
            products_all = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            products_all = paginator.page(1)
        except EmptyPage:
            products_all = paginator.page(paginator.num_pages)

        content = {
            'cart': len(cart), 
            'categories': data,
            'products': products_all,
            'count': products.count(),
            'max': products.aggregate(Max('price')),
            'min': products.aggregate(Min('price')),
            'title': "Список товаров",
            'page': page, 
            'size': size,
            'color': color,
            'category': parent
        }
        return render(request, "mysite/category_detail.html", content)
         

class SearchField(View):

    def get(self, request, *args, **kwargs):  
        data = Category.objects.filter(parent__isnull=True)  
        cart = Cart(request) 
        search_vector = SearchVector('name', 'description')
        search = request.GET.get('search_text') 
        products = Product.objects.annotate(search=search_vector).filter(search=search)
        page = request.GET.get('page')   
        paginator = Paginator(products, 6) 
        try:
            products_all = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            products_all = paginator.page(1)
        except EmptyPage:
            products_all = paginator.page(paginator.num_pages)
 
        content = {
            'cart': len(cart), 
            'categories': data,
            'products': products_all,
            'count': products.count(),
            'max': products.aggregate(Max('price')),
            'min': products.aggregate(Min('price')),
            'title': "Поиск товаров",
            'page': page,  
        }

        return render(request, "mysite/search_result.html", content)


class Checkout(View):

    def post(self, request, *args, **kwargs):
        form = Form_Order(request.POST) 
        if form.is_valid():
            cart = Cart(request)
            name = form.cleaned_data['name']
            recip = settings.EMAIL_HOST_USER
            sender = form.cleaned_data['email']
            city = form.cleaned_data['city']
            user = request.user
            order = Order.objects.create(
                fullname=name, user=user, email=sender, city=city)
            items = []
            for item in cart:
                orderitem = OrderItem.objects.create(
                    order=order, product=item['product'], quantity=item['quantity'], price=item['price'])
                items.append(orderitem)
            cart.clear()
            subject = 'Онлайн-магазин - заказ: {}'.format(order.id)
            context = {
                'order': order,
                'items': items
            }
            template = get_template('mysite/pdf.html')
            html = template.render(context)
            email = EmailMessage(subject, '', sender, [recip])

            pdf = self.render_to_pdf('mysite/pdf.html', context) 
            if not pdf == None: 
                email.attach('order_{}.pdf'.format(order.id),
                             pdf.getvalue(), 'application/pdf')
            else:
                pdf = HttpResponseNotFound(
                    'The requested pdf was not found in our server.')
            email.send()

            return pdf


    def render_to_pdf(self, template_src, context_dict={}):
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")),
                                result, encoding='utf-8', show_error_as_pdf=True)
        if not pdf.err:
            response = HttpResponse(
                result.getvalue(), content_type='application/pdf')
            return response
        return None



class Order(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = Form_Order()
        content = {
            'cart': len(cart),
            'cart_all': cart,
            'title': "Ваш заказ",
            'form': form
        }
        return render(request, "mysite/form_order.html", content)



