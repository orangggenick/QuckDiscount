from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from multiselectfield import MultiSelectField

SEX_SELECT = (
    ('Мужской','Мужской'),
    ('Женский','Женский'),
)

CATEGORIES_SELECT = (
    ('Одежда', 'Одежда'),
    ('Аксессуары', 'Аксессуары'),
    ('Техника', 'Техника'),
    ('Еда', 'Еда'),
    ('Услуги', 'Услуги')
)

STATUS_SELECT = (
    ('сustomer','Покупатель'),
    ('stuff','Владелец магазина'),
)


class DiscountUser(models.Model):
    class Meta():
        db_table = 'DiscountUser'
    user = models.OneToOneField(User)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices=SEX_SELECT, default='Не выбрано')
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)
    categories = MultiSelectField(choices=CATEGORIES_SELECT)
    status = models.CharField(max_length=10, choices=STATUS_SELECT, default='Не выбрано')

    def __str__(self):
        return self.user.username


class DiscountUserForm(ModelForm):
    class Meta():
        model = DiscountUser
        exclude = ['user']


class Shop(models.Model):
    class Meta():
        db_table = 'Shop'
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORIES_SELECT, default='Не выбрано')
    seller_id = models.IntegerField()

    def __str__(self):
        return self.name


class ShopForm(ModelForm):
    class Meta():
        model = Shop
        exclude = ['seller_id']


class Stock(models.Model):
    class Meta():
        db_table = 'Stock'
    exposition = models.CharField(max_length=255)
    terms = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)
    shop_id = models.IntegerField()

    def __str__(self):
        return self.exposition

class StockForm(ModelForm):
    class Meta():
        model = Stock
        exclude = ['shop_id', 'date']


class Subscription(models.Model):
    class Meta():
        db_table = 'subscription'
    user_id = models.IntegerField(null=True)
    shop_id = models.IntegerField(null=True)


class SubscriptionForm(ModelForm):
    class Meta():
        model = Subscription
        exclude = ['user_id', 'shop_id']