from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Reseller(models.Model):
    id = models.CharField(max_length=120, primary_key=True)
    limit = models.IntegerField()
    # owner property is a foreign key related to User instance
    # It is needed to use token authorization
    owner = models.OneToOneField(User)

    def __str__(self):
        return 'Reseller {id}'.format(id=self.id)

    def get_clients_amount(self):
        """
        Calculate clients amount for particular reseller
        """
        return Client.objects.filter(reseller=self).count()

    def get_usage(self):
        """
        Calculate usage of all clients for particular reseller
        """
        total = (Client.objects.filter(reseller=self)
                 .annotate(sum_usage=Sum('clientuser__usage'))
                 .aggregate(Sum('sum_usage')))['sum_usage__sum']
        return total or 0


class Client(models.Model):
    # Instance_id contains company name and used as client id
    id = models.CharField(max_length=150, primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    limit = models.IntegerField()

    # Every client belongs to particular reseller
    reseller = models.ForeignKey(Reseller)

    def __str__(self):
        return 'Client {id}'.format(id=self.id)

    def get_usage(self):
        """
        Calculate total usage of all client users
        """
        total = ClientUser.objects.filter(client=self).aggregate(Sum('usage'))
        return total['usage__sum'] or 0

    def get_users_amount(self):
        """
        Calculate users amount for particular company
        """
        return ClientUser.objects.filter(client=self).count()


class ClientUser(models.Model):
    # email field contains user email and used as user id
    id = models.EmailField(primary_key=True)
    password = models.CharField(max_length=12)
    usage = models.IntegerField(blank=True)
    admin = models.BooleanField(default=False)
    limit = models.IntegerField()
    # Every user belongs to particular client
    client = models.ForeignKey(Client)

    def __str__(self):
        return 'ClientUser {id}'.format(id=self.id)
