from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from filesharing.serializers import ResellerSerializer, CompanySerializer
from filesharing.models import Reseller, Company
from django.shortcuts import render

class ResellerViewSet(viewsets.ModelViewSet):
    queryset = Reseller.objects.all()
    serializer_class = ResellerSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

def resellers(request):
    resellers = Reseller.objects.all()

    return render(request, 'ui/resellers.html', {'resellers': reseller})

def resellercreate(request):
    pass

def reseller(reques):
    pass

def addcompany(request):
    pass

def deletecompany(request):
    pass

def deletereseller(request):
    pass