from django.db import models
from django.db.models import Sum

class Reseller(models.Model):

    def __str__(self):
        return self.instance_id

    def get_clients_amount(self):
        return Client.objects.filter(reseller = self).count()


    def get_usage(self):
        total = 0
        client_list = Client.objects.filter(reseller = self)
        for client in client_list:
            total = total + client.get_usage()
        return total


    instance_id = models.CharField(max_length=120)
    limit = models.IntegerField()
    token = models.CharField(max_length=100)


class Client(models.Model):
    # name contains company name and used as client id
    instance_id = models.CharField(max_length=150)
    creation_date = models.DateTimeField()
    limit = models.IntegerField()
    reseller = models.ForeignKey(Reseller)

    def __str__(self):
        return self.instance_id

    def get_users_amount(self):
        return User.objects.filter(company = self).count()

    def get_usage(self):
        total = User.objects.filter(company = self).aggregate(Sum('usage'))
        if total['usage__sum'] is not None:
            return total['usage__sum']
        else:
            return 0


class User(models.Model):

    def __str__(self):
        return self.instance_id

    # email field contains user email and used as user id
    instance_id = models.EmailField()
    password = models.CharField(max_length=12)
    usage = models.IntegerField()
    admin = models.BooleanField(default=False)
    limit = models.IntegerField()
    company = models.ForeignKey(Client)
