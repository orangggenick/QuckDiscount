from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from Discount.views import home, registration_step1, registration_step2

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'sign_up$', registration_step1, name='registration_step1'),
    url(r'complete_registration$', registration_step2, name='registration_step2'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)