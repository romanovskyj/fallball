from rest_framework import serializers as rest_serializers
from rest_framework.authtoken.models import Token

from .models import Client, Reseller, ClientUser


class StorageResellerSerializer(rest_serializers.HyperlinkedModelSerializer):
    usage = rest_serializers.SerializerMethodField()

    class Meta:
        model = Reseller
        fields = ('usage', 'limit')

    def get_usage(self, obj):
        return obj.get_usage()


class ResellerSerializer(rest_serializers.HyperlinkedModelSerializer):
    storage = StorageResellerSerializer(source='*')
    clients_amount = rest_serializers.SerializerMethodField()
    token = rest_serializers.SerializerMethodField()

    class Meta:
        model = Reseller
        fields = ('id','token', 'clients_amount', 'storage')

    def create(self, validated_data):
        import pdb
        pdb.set_trace()
        return Reseller.objects.create(**validated_data)

    def get_clients_amount(self, obj):
        return obj.get_clients_amount()

    def get_token(self,obj):
        token = Token.objects.filter(user=obj.owner)
        return token[0].key


class StorageClientSerializer(rest_serializers.HyperlinkedModelSerializer):
    usage = rest_serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('usage', 'limit')

    def get_usage(self, obj):
        return obj.get_usage()


class ClientSerializer(rest_serializers.HyperlinkedModelSerializer):
    storage = StorageClientSerializer(source='*')
    users_amount = rest_serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'creation_date', 'users_amount', 'storage')

    def get_users_amount(self, obj):
        return obj.get_users_amount()


class StorageClientUserSerializer(rest_serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClientUser
        fields = ('usage', 'limit')


class ClientUserSerializer(rest_serializers.HyperlinkedModelSerializer):
    role = rest_serializers.SerializerMethodField()
    storage = StorageClientUserSerializer(source='*')

    class Meta:
        model = ClientUser
        fields = ('id', 'password', 'role', 'storage')

    def get_role(self, obj):
        if obj.admin is True:
            return "admin"
        else:
            return "user"

