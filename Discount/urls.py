from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from Discount.views import home, registration_step1, registration_step2, shops, add_shop, logout, login, shop, add_stock, \
    subscribe, unsubscribe, myshops

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'sign_up$', registration_step1, name='registration_step1'),
    url(r'complete_registration$', registration_step2, name='registration_step2'),
    url(r'myshops$', myshops, name='shops'),
    url(r'shops$', shops, name='shops'),
    url(r'add_shop$', add_shop, name='add_shop'),
    url(r'logout$', logout, name='logout'),
    url(r'login$', login, name='login'),
    url(r'shop/(?P<shop_id>\d+)', shop, name='shop'),
    url(r'add_stock/(?P<shop_id>\d+)', add_stock, name='add_stock'),
    url(r'unsubscribe/(?P<shop_id>\d+)', unsubscribe, name='unsubscribe'),
    url(r'subscribe/(?P<shop_id>\d+)', subscribe, name='subscribe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)