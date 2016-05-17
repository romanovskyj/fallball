from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404


def get_object_or_403(*args, **kwargs):
    try:
        result = get_object_or_404(*args, **kwargs)
    except Http404:
        raise PermissionDenied()
    return result
