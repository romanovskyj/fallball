import json
import os

from django.core.exceptions import PermissionDenied,ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Reseller, Client, ClientUser


def get_object_or_403(*args, **kwargs):
    try:
        result = get_object_or_404(*args, **kwargs)
    except Http404:
        raise PermissionDenied()
    return result


def repair(obj):
    """
    Used to repair the object and all his childs to initial state
    """
    # Before repairing objects to initial state
    # it needs to check if object has initial data
    current_dir = os.path.dirname(__file__)
    json_file = os.path.join(current_dir, 'fixtures/dbdump.json')
    with open(json_file) as dbdump:
        data = json.load(dbdump)
        initial_obj = [x for x in data if x['pk'] == obj.pk][0]
        if initial_obj:

            # Delete current data before reparing
            obj.delete()

            # Repair reseller to initial state and itialize reseller clients reparing
            if isinstance(obj, Reseller):
                # Repair initial objects
                Reseller.objects.create(id=initial_obj['pk'],
                                        limit=initial_obj['fields']['limit'],
                                        owner_id=initial_obj['fields']['owner'])
                initial_clients = ([x for x in data if x['model'] == 'fallballapp.client'
                                    and x['fields']['reseller'] == obj.pk])
                for initial_client in initial_clients:
                    client = get_object_or_404(Client, pk=initial_client['pk'])
                    repair(client)

            # Repair client to initial state and initialize clientusers reparing
            elif isinstance(obj, Client):
                Client.objects.create(id=initial_obj['pk'],
                                      creation_date=initial_obj['fields']['creation_date'],
                                      limit=initial_obj['fields']['limit'],
                                      reseller_id=initial_obj['fields']['reseller'])
                initial_client_users = ([x for x in data if x['model'] == 'fallballapp.clientuser'
                                         and x['fields']['client'] == obj.pk])
                for initial_client_user in initial_client_users:
                    client_user = get_object_or_404(Client, pk=initial_client_user['pk'])
                    repair(client_user)

            # Repair clien user
            elif isinstance(obj, ClientUser):
                ClientUser.objects.create(id=obj['pk'],
                                          password=obj['fields']['password'],
                                          usage=obj['fields']['usage'],
                                          admin=obj['fields']['admin'],
                                          limit=obj['fields']['limit'],
                                          client_id=obj['fields']['client'])

            return True

        raise ObjectDoesNotExist()