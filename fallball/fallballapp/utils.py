import json
import os

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Client, ClientUser, Reseller
import fallball.settings as settings

def singleton(f):
    """
    Singleton will avoid multiple times loading file
    """
    cache = [None]

    def wrapper():
        if not cache[0]:
            cache[0] = f()
        return cache[0]

    return wrapper


@singleton
def _get_key():
    """
    Return json objects loaded from file
    """
    key = None

    with open(settings.DBDUMP_FILE,'r') as f:
        key = json.load(f)

    return key


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
    data = _get_key()
    initial_obj = [item for item in data if item['pk'] == pk][0]
    if initial_obj:

        # Delete current data before reparing if the object exists
        model.objects.filter(pk=pk).delete()

        import pdb
        pdb.set_trace()
        # Repair reseller to initial state and itialize reseller clients reparing
        if model is Reseller:
            initial_obj['fields']['owner_id'] = initial_obj['fields'].pop('owner')
            # Repair initial objects
            Reseller.objects.create(id=initial_obj['pk'],
                                    **initial_obj['fields'])
            initial_clients = ([item for item in data if item['model'] == 'fallballapp.client' and
                                item['fields']['reseller'] == pk])
            for initial_client in initial_clients:
                repair(Client, initial_client['pk'])

        # Repair client to initial state and initialize clientusers reparing
        elif model is Client:
            Client.objects.create(id=initial_obj['pk'],
                                  creation_date=initial_obj['fields']['creation_date'],
                                  limit=initial_obj['fields']['limit'],
                                  reseller_id=initial_obj['fields']['reseller'])
            initial_client_users = ([item for item in data if item['model'] == 'fallballapp.clientuser' and
                                     item['fields']['client'] == initial_obj['pk']])
            for initial_client_user in initial_client_users:
                repair(ClientUser, initial_client_user['pk'])

        # Repair client user
        elif model is ClientUser:
            ClientUser.objects.create(id=initial_obj['pk'],
                                      password=initial_obj['fields']['password'],
                                      usage=initial_obj['fields']['usage'],
                                      admin=initial_obj['fields']['admin'],
                                      limit=initial_obj['fields']['limit'],
                                      client_id=initial_obj['fields']['client'])

        return True

    raise ObjectDoesNotExist()


def get_all_resellers():
    """
    Get all resellers from fixture file
    """
    current_dir = os.path.dirname(__file__)
    json_file = os.path.join(current_dir, 'fixtures/dbdump.json')
    with open(json_file) as dbdump:
        data = json.load(dbdump)
        resellers = [item for item in data if item['model'] == 'fallballapp.reseller']
        return resellers
