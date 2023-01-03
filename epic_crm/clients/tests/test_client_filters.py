import pytest

from epic_crm.clients.models import Client


@pytest.mark.django_db
class TestClientFilters:

    def test_clients_without_filter(self, api_client_salesperson):

        Client.objects.create(name='aaaa')
        Client.objects.create(name='bbbb')
        Client.objects.create(name='cccc')

        # --
        response = api_client_salesperson.get('/clients/')
        data = response.json()

        assert len(data) == 3
        assert data[0]['name'] == 'aaaa'
        assert data[1]['name'] == 'bbbb'
        assert data[2]['name'] == 'cccc'

    def test_clients_filter_by_name(self, api_client_salesperson):

        Client.objects.create(name='aaaa')
        Client.objects.create(name='bbbb')
        Client.objects.create(name='cccc')

        # --
        response = api_client_salesperson.get('/clients/?name__contains=b')
        data = response.json()

        assert len(data) == 1
        assert data[0]['name'] == 'bbbb'

    def test_clients_filter_by_email(self, api_client_salesperson):

        Client.objects.create(name='aaaa', email='a@a.com')
        Client.objects.create(name='bbbb', email='b@b.com')
        Client.objects.create(name='cccc', email='c@c.com')

        # --
        response = api_client_salesperson.get('/clients/?email=c@c.com')
        data = response.json()

        assert len(data) == 1
        assert data[0]['name'] == 'cccc'
        # assert data[0]['email'] == 'c@c.com'
