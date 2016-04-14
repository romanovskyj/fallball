from rest_framework import serializers

from .models import Client, Reseller, User

class ResellerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reseller
        fields = ('name', 'usage', 'limit', 'access_token')
