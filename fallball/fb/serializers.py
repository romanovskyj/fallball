from rest_framework import serializers as rest_serializers

from .models import Client, Reseller, User


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

    class Meta:
        model = Reseller
        fields = ('id', 'clients_amount', 'storage')

    def create(self, validated_data):
        return Reseller.objects.create(**validated_data)

    def get_clients_amount(self, obj):
        return obj.get_clients_amount()


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


class StorageUserSerializer(rest_serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('usage', 'limit')


class UserSerializer(rest_serializers.HyperlinkedModelSerializer):
    role = rest_serializers.SerializerMethodField()
    storage = StorageUserSerializer(source='*')

    class Meta:
        model = User
        fields = ('id', 'password','role', 'storage')

    def get_role(self, obj):
        if obj.admin is True:
            return "admin"
        else:
            return "user"
