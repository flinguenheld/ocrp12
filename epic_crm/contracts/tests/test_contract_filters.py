import pytest

from epic_crm.clients.models import Client
from epic_crm.contracts.models import Contract


@pytest.mark.django_db
class TestContractFilters:

    def test_contracts_without_filter(self, api_client_salesperson):

        client_a = Client.objects.create(name='aaaa', email='a@a.com')
        Contract.objects.create(client=client_a)

        client_b = Client.objects.create(name='bbbb', email='b@b.com')
        Contract.objects.create(client=client_b)

        client_c = Client.objects.create(name='cccc', email='c@c.com')
        Contract.objects.create(client=client_c)

        # --
        response = api_client_salesperson.get('/contracts/')
        data = response.json()

        assert len(data) == 3
        assert data[0]['client'] == client_a.pk
        assert data[1]['client'] == client_b.pk
        assert data[2]['client'] == client_c.pk

    def test_contracts_filter_by_client_name(self, api_client_salesperson):

        client_a = Client.objects.create(name='aaaa', email='a@a.com')
        Contract.objects.create(client=client_a)

        client_b = Client.objects.create(name='bbbb', email='b@b.com')
        Contract.objects.create(client=client_b)

        client_c = Client.objects.create(name='cccc', email='c@c.com')
        Contract.objects.create(client=client_c)

        # --
        response = api_client_salesperson.get('/contracts/?client__name=bbbb')
        data = response.json()

        assert len(data) == 1
        assert data[0]['client'] == client_b.pk

    def test_contracts_filter_by_client_email(self, api_client_salesperson):

        client_a = Client.objects.create(name='aaaa', email='a@a.com')
        Contract.objects.create(client=client_a)

        client_b = Client.objects.create(name='bbbb', email='b@b.com')
        Contract.objects.create(client=client_b)

        client_c = Client.objects.create(name='cccc', email='c@c.com')
        Contract.objects.create(client=client_c)

        # --
        response = api_client_salesperson.get('/contracts/?client__email__contains=b')
        data = response.json()

        assert len(data) == 1
        assert data[0]['client'] == client_b.pk

    def test_contracts_filter_by_amount(self, api_client_salesperson):

        client_a = Client.objects.create(name='aaaa', email='a@a.com')
        Contract.objects.create(client=client_a, amount=100)

        client_b = Client.objects.create(name='bbbb', email='b@b.com')
        Contract.objects.create(client=client_b, amount=200)

        client_c = Client.objects.create(name='cccc', email='c@c.com')
        Contract.objects.create(client=client_c, amount=300)

        # --
        response = api_client_salesperson.get('/contracts/?amount=300')
        data = response.json()

        assert len(data) == 1
        assert data[0]['client'] == client_c.pk

        response = api_client_salesperson.get('/contracts/?amount__lte=200')
        data = response.json()

        assert len(data) == 2
        assert data[0]['client'] == client_a.pk
        assert data[1]['client'] == client_b.pk

    def test_contracts_filter_by_date_signed(self, api_client_salesperson):

        client_a = Client.objects.create(name='aaaa', email='a@a.com')
        Contract.objects.create(client=client_a, date_signed='2010-10-10T00:00:00Z')

        client_b = Client.objects.create(name='bbbb', email='b@b.com')
        Contract.objects.create(client=client_b, date_signed='2015-05-15T00:00:00Z')

        client_c = Client.objects.create(name='cccc', email='c@c.com')
        Contract.objects.create(client=client_c, date_signed='2020-02-20T00:00:00Z')

        # --
        response = api_client_salesperson.get('/contracts/?date_signed=2020-02-20')
        data = response.json()

        assert len(data) == 1
        assert data[0]['client'] == client_c.pk

        response = api_client_salesperson.get('/contracts/?date_signed__lte=2016-06-16')
        data = response.json()

        assert len(data) == 2
        assert data[0]['client'] == client_a.pk
        assert data[1]['client'] == client_b.pk
