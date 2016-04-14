from django.db import models


class Reseller(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=120)
    usage = models.IntegerField()
    limit = models.IntegerField()
    token = models.CharField(max_length=100)


class Client(models.Model):
    # name contains company name and used as client id
    name = models.CharField(max_length=150)
    creation_date = models.DateTimeField()
    usage = models.IntegerField()
    limit = models.IntegerField()
    reseller = models.ForeignKey(Reseller)


class User(models.Model):
    # email field contains user email and used as user id
    email = models.EmailField()
    usage = models.IntegerField()
    limit = models.IntegerField()
    company = models.ForeignKey(Client)
