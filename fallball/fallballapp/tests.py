from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from fallballapp.models import Client, Reseller, ClientUser


def _get_client():
    """
    Returns request object with admin token
    """
    client = APIClient()
    # Get admin token and set up credentials
    admin = User.objects.create_superuser('admin', 'admin@fallball.io', '1q2w3e')
    token = get_object_or_404(Token, user=admin)
    client.credentials(HTTP_AUTHORIZATION='Token {token}'.format(token=token.key))
    return client

class BaseTestCase(TestCase):
    """
    Check that resellers, clients, objects can be created and deleted
    """
    def setUp(self):
        self.client = _get_client()

    def test_object_creation(self):
        # create reseller
        self.client.post('/v1/resellers/',
                    '{"id":"test_reseller", "storage":{"limit": 200}}',
                    content_type='application/json')
        # create client
        self.client.post('/v1/resellers/test_reseller/clients/',
                    '{"id":"test_client", "storage":{"limit": 100}}',
                    content_type='application/json')

        # create client user
        self.client.post('/v1/resellers/test_reseller/clients/test_client/users/',
                    '{"id":"test_user@test.tld", "storage":{"limit": 50}, "password": "1q2w3e"}',
                    content_type='application/json')

        # Check that all objects have been created correctly
        self.assertTrue(Reseller.objects.filter(id='test_reseller'))
        self.assertTrue(Client.objects.filter(id='test_client'))
        self.assertTrue(ClientUser.objects.filter(id='test_user@test.tld'))


class ResetTestCase(TestCase):
    pass