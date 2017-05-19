from django.db import models
from django.forms import ModelForm
from multiselectfield import MultiSelectField

SEX_SELECT = (
    ('Мужской','Мужской'),
    ('Женский','Женский'),
)

CATEGORIES_SELECT = (
    ('clothes', 'Одежда'),
    ('accessories', 'Аксессуары'),
    ('tech', 'Техника'),
    ('food', 'Еда'),
    ('services', 'Услуги')
)


class Customer(models.Model):
    class Meta():
        db_table = 'Customer'
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices=SEX_SELECT, default='Не выбрано')
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    categories = MultiSelectField(choices=CATEGORIES_SELECT)


class CustomerForm(ModelForm):
    class Meta():
        model = Customer
        fields = '__all__'


class Seller(models.Model):
    class Meta():
        db_table = 'Seller'
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)


class SellerForm(ModelForm):
    class Meta():
        model = Seller
        fields = '__all__'


class Shop(models.Model):
    class Meta():
        db_table = 'Shop'
    name = models.CharField(max_length=255)
    image = models.ImageField()
    category = models.CharField(max_length=20, choices=CATEGORIES_SELECT, default='Не выбрано')


class ShopForm(ModelForm):
    class Meta():
        model = Shop
        fields = '__all__'


class Stock(models.Model):
    class Meta():
        db_table = 'Stock'
    exposition = models.CharField(max_length=255)
    terms = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)

class StockForm(ModelForm):
    class Meta():
        model = Stock
        fields = '__all__'


class Subscription(models.Model):
    class Meta():
        db_table = 'subscription'
    user_id = models.IntegerField()
    shop_id = models.IntegerField()