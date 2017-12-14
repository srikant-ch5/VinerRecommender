
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^reviews/',include('reviews.urls',namespace="reviews")),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/',include('registration.backends.simple.urls')),
    url(r'^accounts/',include('django.contrib.auth.urls',namespace ="auth")),
]
