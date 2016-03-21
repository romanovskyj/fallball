from filesharing.models import Reseller, Company
from rest_framework import serializers

class ResellerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reseller
        fields = ('partnerid',)

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('resellerid', 'companyname', 'diskusage','admin',)