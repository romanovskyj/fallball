from django.db import models
from django.db.models import Sum


class Reseller(models.Model):
    id = models.CharField(max_length=120,primary_key=True)
    limit = models.IntegerField()
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.instance_id

    def get_clients_amount(self):
        """
        Calculate clients amount for particular reseller
        """
        return Client.objects.filter(reseller=self).count()

    def get_usage(self):
        """
        Calculate usage of all clients for particular reseller
        """
        total = 0
        client_list = Client.objects.filter(reseller=self)
        for client in client_list:
            total = total + client.get_usage()
        return total


class Client(models.Model):
    # Instance_id contains company name and used as client id
    id = models.CharField(max_length=150, primary_key=True)
    creation_date = models.DateTimeField()
    limit = models.IntegerField()

    # Every client belongs to particular reseller
    reseller = models.ForeignKey(Reseller)

    def __str__(self):
        return self.instance_id

    def get_usage(self):
        """
        Calculate total usage amount for particular reseller
        """
        total = User.objects.filter(company=self).aggregate(Sum('usage'))
        if total['usage__sum'] is not None:
            return total['usage__sum']
        else:
            return 0

    def get_users_amount(self):
        """
        Calculate users amount for particular company
        """
        return User.objects.filter(company=self).count()


class User(models.Model):
    # email field contains user email and used as user id
    id = models.EmailField(primary_key=True)
    password = models.CharField(max_length=12)
    usage = models.IntegerField()
    admin = models.BooleanField(default=False)
    limit = models.IntegerField()
    company = models.ForeignKey(Client)

    def __str__(self):
        return self.instance_id
