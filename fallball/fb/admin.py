from django.contrib import admin

from .models import Client, Reseller, User

fb_models = (Client, Reseller, User)
admin.site.register(fb_models)
