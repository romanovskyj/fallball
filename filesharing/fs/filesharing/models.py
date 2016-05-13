from django.db import models
from random import randint
from django.shortcuts import get_list_or_404
from django.db.models import Sum

# Create your models here.

class Reseller(models.Model):

    # Name of the company that will login as reseller
    partnerid = models.CharField(max_length=100)

    def disk_usage(self):
        total = Company.objects.filter(resellerid = self).aggregate(Sum('diskusage'))
        return total['diskusage__sum']

    total = property(disk_usage)

class Company(models.Model):

    # reseller who owns the company
    resellerid = models.ForeignKey(Reseller)

    # name of company who's gonna use the service
    companyname = models.CharField(max_length=100)

    # disk space currently used by company
    diskusage = models.IntegerField(default=randint(100,900))

    # admin of the company
    admin = models.CharField(max_length=120)