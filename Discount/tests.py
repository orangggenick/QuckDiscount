from django.contrib.auth.models import User
from django.test import TestCase

from Discount.models import Shop, Stock, Subscription, Favorites


class CommonTest(TestCase):
    def setUp(self):
        User.objects.create(username="Test", password="qwer1234")
        user = User.objects.get(username="Test")
        Shop.objects.create(name="Test Shop", category="Одежда", seller_id=user.id)
        shop = Shop.objects.get(name="Test Shop")
        Stock.objects.create(exposition="Test exposition", terms="2016-01-02", description="Test description", date="2016-01-01", is_active=True, shop_id=shop.id)


    def test(self):
        user = User.objects.get(username="Test")
        shop = Shop.objects.get(name="Test Shop")
        stock = Stock.objects.get(id = shop.id)
        self.assertEqual(user.id, 1)
        self.assertEqual(shop.name, 'Test Shop')
        self.assertEqual(shop.seller_id, 1)
        self.assertEqual(stock.exposition, 'Test exposition')
        self.assertEqual(stock.shop_id, 1)


class SubscriptionTest(TestCase):
    def setUp(self):
        User.objects.create(username="Test", password="qwer1234")
        user = User.objects.get(username="Test")
        Shop.objects.create(name="Test Shop", category="Одежда", seller_id=user.id)
        shop = Shop.objects.get(name="Test Shop")
        Stock.objects.create(exposition="Test exposition", terms="2016-01-02", description="Test description", date="2016-01-01", is_active=True, shop_id=shop.id)
        Stock.objects.create(exposition="Test exposition2", terms="2016-01-02", description="Test description2",date="2016-01-01", is_active=True, shop_id=shop.id)
        Shop.objects.create(name="Test Shop2", category="Одежда", seller_id=user.id)
        shop2 = Shop.objects.get(name="Test Shop2")
        Stock.objects.create(exposition="Test exposition3", terms="2016-01-02", description="Test description3", date="2016-01-01", is_active=True, shop_id=shop2.id)
        Stock.objects.create(exposition="Test exposition4", terms="2016-01-02", description="Test description4", date="2016-01-01", is_active=True, shop_id=shop2.id)
        Subscription.objects.create(user_id = user.id, shop_id = shop2.id)

    def test(self):
        user = User.objects.get(username="Test")
        subscription = Subscription.objects.get(user_id = user.id)
        stocks = Stock.objects.filter(shop_id=subscription.shop_id)
        self.assertEqual(stocks[0].exposition, "Test exposition3")
        self.assertEqual(stocks[1].exposition, "Test exposition4")


class FavoritesTest(TestCase):
    def setUp(self):
        User.objects.create(username="Test", password="qwer1234")
        user = User.objects.get(username="Test")
        Shop.objects.create(name="Test Shop", category="Одежда", seller_id=user.id)
        shop = Shop.objects.get(name="Test Shop")
        Stock.objects.create(exposition="Test exposition", terms="2016-01-02", description="Test description", date="2016-01-01", is_active=True, shop_id=shop.id)
        Stock.objects.create(exposition="Test exposition2", terms="2016-01-02", description="Test description2",date="2016-01-01", is_active=True, shop_id=shop.id)
        stock1 = Stock.objects.get(exposition="Test exposition")
        stock2 = Stock.objects.get(exposition="Test exposition2")
        Shop.objects.create(name="Test Shop2", category="Одежда", seller_id=user.id)
        shop2 = Shop.objects.get(name="Test Shop2")
        Stock.objects.create(exposition="Test exposition3", terms="2016-01-02", description="Test description3", date="2016-01-01", is_active=True, shop_id=shop2.id)
        Stock.objects.create(exposition="Test exposition4", terms="2016-01-02", description="Test description4", date="2016-01-01", is_active=True, shop_id=shop2.id)
        stock3 = Stock.objects.get(exposition="Test exposition3")
        stock4 = Stock.objects.get(exposition="Test exposition4")
        Favorites.objects.create(user_id = user.id, stock_id = stock2.id)
        Favorites.objects.create(user_id=user.id, stock_id=stock4.id)


    def test(self):
        user = User.objects.get(username="Test")
        favorites = Favorites.objects.filter(user_id = user.id)
        stocks = []
        for favorite in favorites:
            stocks.append(Stock.objects.get(id=favorite.stock_id))
        self.assertEqual(stocks[0].exposition, "Test exposition2")
        self.assertEqual(stocks[1].exposition, "Test exposition4")