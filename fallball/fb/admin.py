from django.contrib import admin

from .models import Client, ClientUser, Reseller

fb_models = (Client, Reseller, ClientUser)
admin.site.register(fb_models)
