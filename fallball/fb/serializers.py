from random import randint

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers as rest_serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

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
        if not User.objects.filter(username=validated_data['id']):
            user = User(username=validated_data['id'])
            user.save()
            Token.objects.create(user=user)
            return Reseller.objects.create(owner=user, **validated_data)
        else:
            raise ValidationError('Reseller with such id is already created')

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

    def create(self, validated_data):
        return Client.objects.create(reseller=self.initial_data['reseller'], **validated_data)

    def get_users_amount(self, obj):
        return obj.get_users_amount()


class StorageClientUserSerializer(rest_serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ClientUser
        fields = ('usage', 'limit')


class ClientUserSerializer(rest_serializers.ModelSerializer):
    role = rest_serializers.SerializerMethodField()
    storage = StorageClientUserSerializer(source='*')
    #client = rest_serializers.SerializerMethodField()

    class Meta:
        model = ClientUser
        fields = ('id', 'client', 'password', 'role', 'storage')

    def create(self, validated_data):
        usage = randint(0, validated_data['limit'])
        return ClientUser.objects.create(usage=usage, **validated_data)

    def get_role(self, obj):
        if obj.admin is True:
            return "admin"
        else:
            return "user"

