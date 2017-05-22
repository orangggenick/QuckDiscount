from django.contrib import admin

from Discount.models import DiscountUser, Shop, Stock, Subscription

admin.site.register(DiscountUser)
admin.site.register(Shop)
admin.site.register(Stock)
admin.site.register(Subscription)
