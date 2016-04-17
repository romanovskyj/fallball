from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from fb.views import ClientViewSet, ResellerViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'resellers', ResellerViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'resellers', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
