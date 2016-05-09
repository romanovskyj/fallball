from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^v1/', include('fallballapp.urls', namespace='v1')),
    url(r'^admin/', admin.site.urls),
]
