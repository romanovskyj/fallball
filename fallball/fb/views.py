from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Client, Reseller, ClientUser
from .serializers import ClientSerializer, ResellerSerializer, ClientUserSerializer


class ResellerViewSet(viewsets.ModelViewSet):
    """
    To get list of resellers or create new reseller
    admin token should be specified
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ResellerSerializer
    queryset = Reseller.objects.all()



class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-id')
    serializer_class = ClientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        reseller = get_object_or_404(Reseller,owner=request.user)
        queryset = Client.objects.filter(reseller=reseller)
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        request.data['creation_date'] = datetime.now()
        request.data['reseller'] = get_object_or_404(Reseller,owner=request.user)
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientUserViewSet(viewsets.ModelViewSet):
    queryset = ClientUser.objects.all().order_by('-id')
    serializer_class = ClientUserSerializer


