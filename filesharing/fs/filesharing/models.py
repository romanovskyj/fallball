from django.db import models
from random import randint

# Create your models here.

class Reseller(models.Model):

    # Name of the company that will login as reseller
    partnerid = models.CharField(max_length=100)

    def disk_usage(self):
        pass

class Company(models.Model):

    # reseller who owns the company
    resellerid = models.ForeignKey(Reseller)

    # name of company who's gonna use the service
    companyname = models.CharField(max_length=100)

    # disk space currently used by company
    diskusage = models.IntegerField(default=randint(100,900))

    # admin of the company
    admin = models.CharField(max_length=120)