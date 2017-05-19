from django.contrib import admin

from Discount.models import Customer, Seller, Shop, Stock, Subscription

admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Shop)
admin.site.register(Stock)
admin.site.register(Subscription)
