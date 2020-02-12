from django.db import models
from django.contrib.auth.models import User
from slugify import slugify
from phone_field import PhoneField
from django.db.models.signals import post_save, pre_save


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta: 
        verbose_name_plural = "categories"

    def __str__(self):        
        return self.name 

    def save(self, *args, **kw): 
        self.slug = _get_unique_slug(self, Category) 
        super(Category, self).save(*args, **kw)

    def get_children(self):
        return Category.objects.filter(parent_id=self)

    def is_child(self):
        return self.parent


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True) 
    description = models.TextField(blank=True, null=True, verbose_name="Полное описание") 
    price = models.DecimalField(blank=True, null=True, max_digits=7, decimal_places=2)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def get_image(self):
        obj = Gallery.objects.filter(product=self, image_main=True)
        if not obj.exists():
            return None 
        return obj[0].image.url

    def get_image_all(self):
        obj = Gallery.objects.filter(product=self).exclude(image_main=True)
        if not obj.exists():
            return None 
        return obj

    def get_feature(self):
        obj = Feature.objects.filter(product=self)
        if not obj.exists():
            return None 
        return obj

    def save(self, *args, **kw):
       self.slug = _get_unique_slug(self, Product) 
       super(Product, self).save(*args, **kw)


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField()
    image_main = models.BooleanField(blank=True, null=True)

class StatusOrder(models.Model):
    name = models.CharField(blank=True, null=True, max_length=100)

    class Meta:
        db_table = "StatusOrder"

class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fullname = models.CharField(blank=True, null=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    email = models.EmailField(blank=True, null=True,)
    city = models.CharField(blank=True, null=True, max_length=100)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    status = models.ForeignKey(StatusOrder, blank=True, null=True,  on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order: {}'.format(self.id)

    def get_total(self):
        orders = OrderItem.objects.filter(order=self)
        sum = 0
        for item in orders:
            sum += item.get_cost()
        self.total_price = sum


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    price = models.DecimalField(blank=True, null=True, max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(blank=True, null=True, default=1)  


    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):  
        if (self.price==None):
            self.price = self.product.price
            self.save()
        elif int(self.price)==0:
            self.price = self.product.price
            self.save()
        return self.price * self.quantity


class Size(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "Size"

    def __str__(self):
        return '{}'.format(self.name)

class Color(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "Color"

    def __str__(self):
        return '{}'.format(self.name)

class SizeFeature(models.Model):
    size = models.ForeignKey(Size, default=1, blank=True, null=True, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, blank=True, null=True,  on_delete=models.CASCADE) 

    def __str__(self):
        return '{}'.format(self.size)

class ColorFeature(models.Model):
    color = models.ForeignKey(Color, default=1, blank=True, null=True, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.color)
  

def _get_unique_slug(instance, modelName): 
    slug = slugify(instance.name.lower())
    unique_slug = slug
    num = 1
    while modelName.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1 
    return unique_slug 


def total_order(sender, instance, created, **kwargs):  
    instance.order.get_total()
    instance.order.save()


post_save.connect(total_order, sender=OrderItem)