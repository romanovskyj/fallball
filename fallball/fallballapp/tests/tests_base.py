from django.contrib.auth.models import User
from django.core.management import call_command
from django.shortcuts import get_object_or_404
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from fallballapp.models import Client, ClientUser, Reseller


def _get_client():
    """
    Returns request object with admin token
    """
    client = APIClient()
    # Get admin token and set up credentials
    admin = User.objects.filter(username='admin').first()
    if not admin:
        admin = User.objects.create_superuser('admin', 'admin@fallball.io', '1q2w3e')
    token = get_object_or_404(Token, user=admin)
    client.credentials(HTTP_AUTHORIZATION='Token {token}'.format(token=token.key))
    return client


class BaseTestCase(TestCase):
    """
    Test basic operations: model objects create/delete
    """

    # Check that resellers, clients, objects can be created and deleted
    @classmethod
    def setUpTestData(cls):
        cls.client_request = _get_client()

    def test_object_creation(self):
        # create reseller
        self.client_request.post('/v1/resellers/',
                                 '{"id":"test_reseller", "storage":{"limit": 200}}',
                                 content_type='application/json')
        # create client
        self.client_request.post('/v1/resellers/test_reseller/clients/',
                                 '{"id":"test_client", "storage":{"limit": 100}}',
                                 content_type='application/json')

        # create client user
        self.client_request.post('/v1/resellers/test_reseller/clients/test_client/users/',
                                 '{"id":"test_user@test.tld", "storage":{"limit": 50}, "password": "1q2w3e"}',
                                 content_type='application/json')

        # Check that all objects have been created correctly
        self.assertTrue(Reseller.objects.filter(id='test_reseller'))
        self.assertTrue(Client.objects.filter(id='test_client'))
        self.assertTrue(ClientUser.objects.filter(id='test_user@test.tld'))

    def test_object_recreation(self):
        self.client_request.post('/v1/resellers/',
                                 '{"id":"RecreationReseller", "storage":{"limit": 200}}',
                                 content_type='application/json')
        self.client_request.delete('/v1/resellers/RecreationReseller', content_type='application/json')
        self.client_request.post('/v1/resellers/',
                                 '{"id":"RecreationReseller", "storage":{"limit": 200}}',
                                 content_type='application/json')


class ResetTestCase(TestCase):
    """
    Test reset methods
    """

    @classmethod
    def setUpTestData(cls):
        cls.client_request = _get_client()

    def setUp(self):
        # reload initial data
        call_command('loaddata', 'dbdump')

    def test_reset_all_resellers(self):
        # delete reseller that should be available initially
        Reseller.objects.filter(id='reseller_b').delete()

        # Create new reseller to be aware it is delete after the /rest calling
        self.client_request.post('/v1/resellers/',
                                 '{"id":"test_reset_reseller", "storage":{"limit": 300}}',
                                 content_type='application/json')

        self.client_request.get('/v1/resellers/reset_all/')

        self.assertTrue(Reseller.objects.filter(id='reseller_a'))
        self.assertTrue(Reseller.objects.filter(id='reseller_b'))
        self.assertFalse(Reseller.objects.filter(id='reseller_reset_reseller'))

    def test_reset_reseller(self):
        Client.objects.filter(id='SunnyFlowers').delete()
        self.client_request.get('/v1/resellers/reseller_a/reset/')

        # check that not only client but its parent objects were also repaired
        self.assertTrue(Client.objects.filter(id='SunnyFlowers'))
        self.assertTrue(ClientUser.objects.filter(id='brown@sunnyflowers.tld'))

    def test_reset_all_clients(self):
        Client.objects.filter(id='SunnyFlowers').delete()
        self.client_request.post('/v1/resellers/reseller_a/clients/',
                                 '{"id":"test_client", "storage":{"limit": 100}}',
                                 content_type='application/json')

        self.client_request.get('/v1/resellers/reseller_a/clients/reset_all/')

        # check that not only reseller but its parent objects were also repaired
        self.assertTrue(Client.objects.filter(id='SunnyFlowers'))
        self.assertTrue(ClientUser.objects.filter(id='brown@sunnyflowers.tld'))
        self.assertFalse(Client.objects.filter(id='test_client'))

    def test_reset_client(self):
        ClientUser.objects.filter(id='brown@sunnyflowers.tld').delete()
        self.client_request.post('/v1/resellers/reseller_a/clients/SunnyFlowers/users/',
                                 '{"id":"test_user@sunnyflowers.tld", "storage":{"limit": 50}, "password": "1q2w3e"}',
                                 content_type='application/json')

        self.client_request.get('/v1/resellers/reseller_a/clients/SunnyFlowers/reset/')

        self.assertTrue(ClientUser.objects.filter(id='brown@sunnyflowers.tld'))
        self.assertFalse(ClientUser.objects.filter(id='test_user@sunnyflowers.tld'))
