from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Client, ClientUser, Reseller
from .serializers import (ClientSerializer, ClientUserSerializer,
                          ResellerSerializer)


class ResellerViewSet(ModelViewSet):
    """
    ViewSet that manages resellers.
    Only admin token allows managing resellers
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ResellerSerializer
    queryset = Reseller.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ModelViewSet.create(self, request, *args, **kwargs)
        return Response("Only superuser can create reseller", status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        """
        Method is overwritten in order to implement superuser check
        """
        if request.user.is_superuser:
            return ModelViewSet.list(self, request, *args, **kwargs)
        return Response("Only superuser can get resellers list", status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ModelViewSet.retrieve(self, request, *args, **kwargs)
        return Response("Only superuser can get reseller information", status=status.HTTP_403_FORBIDDEN)


class ClientViewSet(ModelViewSet):
    """
    ViewSet which manages clients
    """
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """
        Create new reseller client
        """
        if request.user.is_superuser:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'])[0]
        else:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'], owner=request.user)[0]

        if reseller:
            # Get current date to add it to client.creation_date
            request.data['creation_date'] = datetime.now()
            # Every client should belong to particular reseller
            request.data['reseller'] = reseller
            return ModelViewSet.create(self, request, *args, **kwargs)

        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)

    def list(self, request, **kwargs):
        """
        Return list of clients which owned by particular reseller
        """

        # If admin token is provided we just get reseller from the database
        # If reseller token is provided we need to check that clients are owned by this reseller
        if request.user.is_superuser:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'])
        else:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'], owner=request.user)

        if reseller:
            queryset = Client.objects.filter(reseller=reseller[0])
            serializer = ClientSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        """
        Return particular client which owned by particular reseller
        """
        if request.user.is_superuser:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'])
        else:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'], owner=request.user)

        if reseller:
            return ModelViewSet.retrieve(self, request, *args, **kwargs)

        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class ClientUserViewSet(ModelViewSet):
    """
    Create new client user
    """
    queryset = ClientUser.objects.all().order_by('-id')
    serializer_class = ClientUserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # Redefine regex in order to get user email as id
    lookup_value_regex = '[-\w]+(?:\@)?[A-Za-z0-9.-]+(?:\.)?[A-Za-z]{2,4}'

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'])
        else:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'], owner=request.user)

        if reseller:
            # get client to provide it for user creation
            client = Client.objects.filter(reseller=reseller, id=kwargs['client_pk'])
            if client:
                request.data['client'] = client[0].id
                return ModelViewSet.create(self, request, *args, **kwargs)

        return Response('Current reseller does not have permissions for this client', status=status.HTTP_403_FORBIDDEN)

    def list(self, request, **kwargs):
        if request.user.is_superuser:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'])
        else:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'], owner=request.user)

        if reseller:
            client = get_object_or_404(Client, reseller=reseller, id=kwargs['client_pk'])
            queryset = ClientUser.objects.filter(client=client)
            serializer = ClientUserSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_superuser:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'])
        else:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'], owner=request.user)

        if reseller:
            return ModelViewSet.retrieve(self, request, *args, **kwargs)
        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)
