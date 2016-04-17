from rest_framework import viewsets

from .models import Reseller, Client, User
from .serializers import ClientSerializer, ResellerSerializer, UserSerializer


class ResellerViewSet(viewsets.ModelViewSet):
    queryset = Reseller.objects.all().order_by('-id')
    serializer_class = ResellerSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer