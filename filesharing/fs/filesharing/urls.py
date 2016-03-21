from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^resellers/', views.resellers, name='resellers_list'),
    url(r'^resellers/new/', views.resellercreate, name='resellers_new'),
    url(r'^resellers/(?P<reseller_id>[0-9]+)/$', views.reseller, name='reseller'),
    url(r'^resellers/(?P<reseller_id>[0-9]+)/delete$', views.deletereseller),
    url(r'^resellers/(?P<reseller_id>[0-9]+)/addcompany$', views.addcompany),
    url(r'^resellers/(?P<reseller_id>[0-9]+)/(?P<company_id>[0-9]+)/deletey$', views.deletecompany),
]