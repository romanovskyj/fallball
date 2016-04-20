from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Client, Reseller, User
from .serializers import ClientSerializer, ResellerSerializer, UserSerializer


class ResellerViewSet(viewsets.ModelViewSet):
    # To get list of resellers or create new reseller
    # admin token should be specified
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Reseller.objects.all().order_by('-id')
    serializer_class = ResellerSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
