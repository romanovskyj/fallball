from random import randint

from django.contrib.auth.models import User
from rest_framework import serializers as rest_serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from fallballapp.models import Client, ClientUser, Reseller


class StorageResellerSerializer(rest_serializers.HyperlinkedModelSerializer):
    """
    Auxiliary serializer in order to make nested json: "storage": {"usage","limit"}
    """
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
        fields = ('id', 'token', 'clients_amount', 'storage')

    def create(self, validated_data):
        """
        This method is overwritten in order to create User object and associate it with reseller.
        This operation is needed to create token for reseller
        """
        if User.objects.filter(username=validated_data['id']).exists():
            raise ValidationError('Reseller with such id is already created')

        user = User.objects.create(username=validated_data['id'])
        return Reseller.objects.create(owner=user, **validated_data)

    def get_clients_amount(self, obj):
        return obj.get_clients_amount()

    def get_token(self, obj):
        """
        As token exists inside User object, we need to get it to show it with particular reseller
        """
        token = Token.objects.filter(user=obj.owner).first()
        return token.key if token else None


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
        """
        Method is overwritten as we need to associate user with reseller
        """
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

    class Meta:
        model = ClientUser
        fields = ('id', 'client', 'password', 'role', 'storage')

    def create(self, validated_data):
        # Usage is random but not more than limit
        usage = randint(0, validated_data['limit'])
        user = User.objects.create_user(username=validated_data['id'], password=validated_data['password'])
        return ClientUser.objects.create(usage=usage, user=user, **validated_data)

    def get_role(self, obj):
        if obj.admin:
            return "admin"
        return "user"


class UserSerializer(rest_serializers.ModelSerializer):
    pass
