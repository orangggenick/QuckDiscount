from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from Discount.views import home, registration_step1, registration_step2, shops, add_shop, logout, login, shop, add_stock, \
    subscribe, unsubscribe, myshops, mysubscripthons, cabinet, change_logo, change_stock, delete_stock, add_to_favorites, \
    myfavorites, delete_from_favorites

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
    url(r'mysubscripthons$', mysubscripthons, name='mysubscripthons'),
    url(r'myfavorites$', myfavorites, name='myfavorites'),
    url(r'subscribe/(?P<shop_id>\d+)', subscribe, name='subscribe'),
    url(r'cabinet', cabinet, name='cabinet'),
    url(r'change_logo/(?P<shop_id>\d+)$', change_logo, name='change_logo'),
    url(r'change_stock/(?P<stock_id>\d+)$', change_stock, name='change_stock'),
    url(r'delete_stock/(?P<stock_id>\d+)$', delete_stock, name='delete_stock'),
    url(r'add_to_favorites/(?P<stock_id>\d+)$', add_to_favorites, name='add_to_favorites'),
    url(r'delete_from_favorites/(?P<stock_id>\d+)$', delete_from_favorites, name='delete_from_favorites'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)