import json
import os

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

import fallball.settings as settings

from .models import Client, ClientUser, Reseller


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

    return dump


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

        # Prepere initial object for model creation
        initial_obj = prepare_dict_for_model(initial_obj)

        # Repair reseller to initial state and itialize reseller clients reparing
        if model is Reseller:
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
    data = _get_dump()
    resellers = [item for item in data if item['model'] == 'fallballapp.reseller']
    return resellers


def prepare_dict_for_model(d):
    """
    Prepare some keys of dict to sent the dict for model creation
    """
    if 'owner' in d:
        d['owner_id'] = d['fields'].pop('owner')
    if 'reseller' in d:
        d['reseller_id'] = d['fields'].pop('reseller')
    if 'client' in d:
        d['client_id'] = d['fields'].pop('client')

    return d