import json

from rest_framework import serializers as rest_serializers

from .models import Client, Reseller, User


class StorageSerializer(rest_serializers.HyperlinkedModelSerializer):
    usage = rest_serializers.SerializerMethodField()

    class Meta:
        model = Reseller
        fields = ('usage','limit',)

    def get_usage(self,obj):
        return obj.get_usage()

class ResellerSerializer(rest_serializers.HyperlinkedModelSerializer):
    storage = StorageSerializer(source='*')
    clients_amount = rest_serializers.SerializerMethodField()

    class Meta:
        model = Reseller
        fields = ('instance_id', 'storage', 'token', 'clients_amount')

    def get_clients_amount(self,obj):
        return obj.get_clients_amount()