from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Client, Reseller, ClientUser
from .serializers import ClientSerializer, ResellerSerializer, ClientUserSerializer


class ResellerViewSet(ModelViewSet):
    """
    To get list of resellers or create new reseller
    admin token should be specified
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ResellerSerializer
    queryset = Reseller.objects.all()

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ModelViewSet.list(self, request, *args, **kwargs)
        return Response("Only superuser can get resellers list", status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ModelViewSet.retrieve(self, request, *args, **kwargs)
        return Response("Only superuser can get resellers list", status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return ModelViewSet.create(self, request, *args, **kwargs)
        return Response("Only superuser can create reseller", status=status.HTTP_403_FORBIDDEN)


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, **kwargs):
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
        reseller = Reseller.objects.filter(id=kwargs['reseller_pk'], owner=request.user)
        if reseller:
            return ModelViewSet.retrieve(self, request, *args, **kwargs)
        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'])
        else:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'], owner=request.user)
        if reseller:
            request.data['creation_date'] = datetime.now()
            request.data['reseller'] = get_object_or_404(Reseller,id=kwargs['reseller_pk'])
            return ModelViewSet.create(self, request, *args, **kwargs)
        return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)


class ClientUserViewSet(ModelViewSet):
    queryset = ClientUser.objects.all().order_by('-id')
    serializer_class = ClientUserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_value_regex = '[-\w]+(?:\@)?[A-Za-z0-9.-]+(?:\.)?[A-Za-z]{2,4}'

    def list(self, request, **kwargs):
        if request.user.is_superuser:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'])
        else:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'], owner=request.user)
        if reseller:
            client = get_object_or_404(Client,reseller=reseller, id=kwargs['client_pk'])
            queryset = ClientUser.objects.filter(client=client)
        serializer = ClientUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'])
        else:
            reseller = Reseller.objects.filter(id=kwargs['reseller_pk'], owner=request.user)
        if reseller:
            client = Client.objects.filter(reseller=reseller,id=kwargs['client_pk'])
            if client:
                request.data['client'] = client[0].id
                return ModelViewSet.create(self, request, *args, **kwargs)
        return Response('Current reseller does not have permissions for this client', status=status.HTTP_403_FORBIDDEN)