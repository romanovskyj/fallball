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


def repair(model, pk):
    """
    Used to repair the object and all his childs to initial state
    """
    # Before repairing objects to initial state
    # it needs to check if object has initial data
    current_dir = os.path.dirname(__file__)
    json_file = os.path.join(current_dir, 'fixtures/dbdump.json')
    with open(json_file) as dbdump:
        data = json.load(dbdump)
        initial_obj = [x for x in data if x['pk'] == pk][0]
        if initial_obj:

            # Delete current data before reparing if the object exists
            obj = model.objects.filter(pk=pk).first()
            obj.delete() if obj else None

            # Repair reseller to initial state and itialize reseller clients reparing
            if model == Reseller:
                # Repair initial objects
                Reseller.objects.create(id=initial_obj['pk'],
                                        limit=initial_obj['fields']['limit'],
                                        owner_id=initial_obj['fields']['owner'])
                initial_clients = ([x for x in data if x['model'] == 'fallballapp.client'
                                    and x['fields']['reseller'] == pk])
                for initial_client in initial_clients:
                    repair(Client, initial_client['pk'])

            # Repair client to initial state and initialize clientusers reparing
            elif model == Client:
                Client.objects.create(id=initial_obj['pk'],
                                      creation_date=initial_obj['fields']['creation_date'],
                                      limit=initial_obj['fields']['limit'],
                                      reseller_id=initial_obj['fields']['reseller'])
                initial_client_users = ([x for x in data if x['model'] == 'fallballapp.clientuser'
                                         and x['fields']['client'] == initial_obj['pk']])
                for initial_client_user in initial_client_users:
                    repair(ClientUser, initial_client_user['pk'])

            # Repair client user
            elif model == ClientUser:
                ClientUser.objects.create(id=initial_obj['pk'],
                                          password=initial_obj['fields']['password'],
                                          usage=initial_obj['fields']['usage'],
                                          admin=initial_obj['fields']['admin'],
                                          limit=initial_obj['fields']['limit'],
                                          client_id=initial_obj['fields']['client'])

            return True

        raise ObjectDoesNotExist()