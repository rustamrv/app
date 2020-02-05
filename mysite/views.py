from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, ListView, DetailView, CreateView
from .models import Category, Product, Gallery, OrderItem, Order, Size, ColorFeature
from django.conf import settings
from .cart import Cart
from .forms import Form_Order
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO 
from django.db.models import Max, Min, Q



class MarketList(ListView):

    model = Category
    template = 'category_list.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = Category.objects.filter(parent__isnull=True)
        products = Product.objects.filter(parent__isnull=True)
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
        products = Product.objects.filter(parent=self.get_object()).order_by('price')
        cart = Cart(self.request)
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')
        size = Size.objects.all()
        color = ColorFeature.objects.all()

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
        product.get_image_all()
        context = super().get_context_data(**kwargs)
        context['instance'] = product
        context['title'] = str(product)
        return context


def add_item(request):
    if request.method == "GET":
        quantity = request.GET.get('quantity')
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product, quantity, True)
        data = Category.objects.filter(parent__isnull=True)
        products = Product.objects.filter(parent=product.parent).order_by('price')
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


def delete_item(request):
    if request.method == "GET":
        cart = Cart(request)
        product_id = request.GET.get('product_id')
        cart.remove(product_id)

        content = {
            'cart': len(cart),
            'cart_all': cart,
            'title': "Ваша корзина"
        }
        return render(request, "mysite/cart_list.html", content)


def cart_list(request):
    if request.method == "GET":
        cart = Cart(request)
        content = {
            'cart': len(cart),
            'cart_all': cart,
            'title': "Ваша корзина"
        }
        return render(request, "mysite/cart_list.html", content)


def filter_shop(request): 
    if request.method == "GET": 
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to') 
        name_category = request.GET.get('category') 
        parent = Category.objects.get(name=name_category)
        products = Product.objects.filter(parent=parent).filter(Q(price__gte=price_from) & Q(price__lte=price_to))
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
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
            'title': "Список товаров",
            'page': page 
        }
        return render(request, "mysite/category_detail.html", content)


def checkout(request):
    if request.method == "POST":
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
            template = get_template('market/pdf.html')
            html = template.render(context)
            email = EmailMessage(subject, '', sender, [recip])

            pdf = render_to_pdf('market/pdf.html', context)
             
            if not pdf == None:
                email.attach('order_{}.pdf'.format(order.id),
                             pdf.getvalue(), 'application/pdf')
            else:
                pdf = HttpResponseNotFound(
                    'The requested pdf was not found in our server.')
            email.send()

            return pdf


def form_order(request):
    if request.method == "GET":
        cart = Cart(request)
        form = Form_Order()
        content = {
            'cart': len(cart),
            'cart_all': cart,
            'title': "Ваш заказ",
            'form': form
        }
        return render(request, "mysite/form_order.html", content)


def render_to_pdf(template_src, context_dict={}):
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
