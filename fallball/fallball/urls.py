from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from fb.views import ResellerViewSet

router = routers.DefaultRouter()
router.register(r'resellers', ResellerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
