import json

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

import fallball.settings as settings
from fallballapp.models import Client, ClientUser, Reseller


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
def _get_dump():
    """
    Return json objects loaded from file
    """
    dump = None

    with open(settings.DBDUMP_FILE, 'r') as f:
        dump = json.load(f)
        data = []

        # Correct dump to prepare it for model object creation
        for item in dump:
            data.append(prepare_dict_for_model(item))

    return data


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
    data = _get_dump()
    initial_obj = [item for item in data if item['pk'] == pk][0]
    if initial_obj:
        # Delete current data before reparing if the object exists
        model.objects.filter(pk=pk).delete()

        # Repair reseller to initial state and itialize reseller clients reparing
        if model is Reseller:
            # Repair initial objects
            Reseller.objects.create(id=initial_obj['pk'],
                                    **initial_obj['fields'])

            # Delete all clients that exist for this reseller
            Client.objects.filter(reseller_id=initial_obj['pk']).delete()

            initial_clients = ([item for item in data if item['model'] == 'fallballapp.client' and
                                item['fields']['reseller_id'] == pk])
            for initial_client in initial_clients:
                repair(Client, initial_client['pk'])

        # Repair client to initial state and initialize clientusers reparing
        elif model is Client:
            Client.objects.create(id=initial_obj['pk'],
                                  **initial_obj['fields'])

            # Delete all users that exist for this client
            ClientUser.objects.filter(client_id=initial_obj['pk']).delete()

            initial_client_users = ([item for item in data if item['model'] == 'fallballapp.clientuser' and
                                     item['fields']['client_id'] == initial_obj['pk']])
            for initial_client_user in initial_client_users:
                repair(ClientUser, initial_client_user['pk'])

        # Repair client user
        elif model is ClientUser:
            ClientUser.objects.create(id=initial_obj['pk'],
                                      **initial_obj['fields'])

        return True

    raise ObjectDoesNotExist()


def get_all_resellers():
    """
    Get all resellers from fixture file
    """
    data = _get_dump()
    resellers = [item for item in data if item['model'] == 'fallballapp.reseller']
    return resellers


def get_all_reseller_clients(reseller_pk):
    """
    Get all resellers from fixture file
    """
    data = _get_dump()
    clients = [item for item in data if item['model'] == 'fallballapp.client' and
               item['fields']['reseller_id'] == reseller_pk]
    return clients


def prepare_dict_for_model(item):
    """
    Prepare some keys of dict to sent the dict for model creation
    """
    for field in ['owner', 'reseller', 'client']:
        if field in item['fields']:
            item['fields']['{}_id'.format(field)] = item['fields'].pop(field)

    return item


def dump_exits(pk):
    """
    Only objects that have dump can be repaired
    """
    data = _get_dump()
    if [item for item in data if item['pk'] == pk]:
        return True
    return False
