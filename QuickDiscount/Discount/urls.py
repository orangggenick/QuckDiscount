from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from Discount.views import home

urlpatterns = [
    url(r'^$', home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)