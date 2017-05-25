from django.contrib import admin

from Discount.models import DiscountUser, Shop, Stock, Subscription, Favorites

admin.site.register(DiscountUser)
admin.site.register(Shop)
admin.site.register(Stock)
admin.site.register(Subscription)
admin.site.register(Favorites)

