import binascii
from datetime import datetime
import os

from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Client, Reseller, User, ResellerUser
from .serializers import ClientSerializer, ResellerSerializer, UserSerializer, ResellerUserSerializer


class ResellerViewSet(viewsets.ModelViewSet):
    """
    To get list of resellers or create new reseller
    admin token should be specified
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Reseller.objects.all().order_by('-id')
    serializer_class = ResellerSerializer

    def create(self, request):
        token = binascii.hexlify(os.urandom(20)).decode()
        request.data['token'] = token
        serializer = ResellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer

    def create(self, request):
        request.data['creation_date'] = datetime.now()
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer


