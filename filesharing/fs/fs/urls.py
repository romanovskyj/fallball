from django.conf.urls import url, include
from rest_framework import routers
from filesharing import views

router = routers.DefaultRouter()
router.register(r'resellers', views.ResellerViewSet)
router.register(r'companies', views.CompanyViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'ui/', include('filesharing.urls')),
]