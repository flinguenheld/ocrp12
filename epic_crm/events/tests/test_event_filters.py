import pytest

from epic_crm.clients.models import Client
from epic_crm.contracts.models import Contract
from epic_crm.events.models import Event


@pytest.mark.django_db
class TestEventFilters:

    def test_event_without_filter(self, api_client_salesperson):

        client_a = Client.objects.create(name='aaaa', email='a@a.com')
        contract_a = Contract.objects.create(client=client_a)
        Event.objects.create(name='aa', contract=contract_a, date='2015-05-15T00:00:00Z')

        client_b = Client.objects.create(name='bbbb', email='b@b.com')
        contract_b = Contract.objects.create(client=client_b)
        Event.objects.create(name='bb', contract=contract_b, date='2020-02-20T00:00:00Z')

        client_c = Client.objects.create(name='cccc', email='c@c.com')
        contract_c = Contract.objects.create(client=client_c)
        Event.objects.create(name='cc', contract=contract_c, date='2025-05-25T00:00:00Z')

        # --
        response = api_client_salesperson.get('/events/')
        data = response.json()

        assert len(data) == 3
        assert data[0]['contract'] == contract_a.pk
        assert data[1]['contract'] == contract_b.pk
        assert data[2]['contract'] == contract_c.pk

    def test_event_filter_by_client_name(self, api_client_salesperson):

        client_a = Client.objects.create(name='aaaa', email='a@a.com')
        contract_a = Contract.objects.create(client=client_a)
        Event.objects.create(name='aa', contract=contract_a, date='2015-05-15T00:00:00Z')

        client_b = Client.objects.create(name='bbbb', email='b@b.com')
        contract_b = Contract.objects.create(client=client_b)
        Event.objects.create(name='bb', contract=contract_b, date='2020-02-20T00:00:00Z')

        client_c = Client.objects.create(name='cccc', email='c@c.com')
        contract_c = Contract.objects.create(client=client_c)
        Event.objects.create(name='cc', contract=contract_c, date='2025-05-25T00:00:00Z')

        # --
        response = api_client_salesperson.get('/events/?contract__client__name=aaaa')
        data = response.json()

        assert len(data) == 1
        assert data[0]['contract'] == contract_a.pk

    def test_event_filter_by_client_email(self, api_client_salesperson):

        client_a = Client.objects.create(name='aaaa', email='a@a.com')
        contract_a = Contract.objects.create(client=client_a)
        Event.objects.create(name='aa', contract=contract_a, date='2015-05-15T00:00:00Z')

        client_b = Client.objects.create(name='bbbb', email='b@b.com')
        contract_b = Contract.objects.create(client=client_b)
        Event.objects.create(name='bb', contract=contract_b, date='2020-02-20T00:00:00Z')

        client_c = Client.objects.create(name='cccc', email='c@c.com')
        contract_c = Contract.objects.create(client=client_c)
        Event.objects.create(name='cc', contract=contract_c, date='2025-05-25T00:00:00Z')

        # --
        response = api_client_salesperson.get('/events/?contract__client__name__contains=b')
        data = response.json()

        assert len(data) == 1
        assert data[0]['contract'] == contract_b.pk

    def test_event_filter_by_date(self, api_client_salesperson):

        client_a = Client.objects.create(name='aaaa', email='a@a.com')
        contract_a = Contract.objects.create(client=client_a)
        Event.objects.create(name='aa', contract=contract_a, date='2015-05-15T00:00:00Z')

        client_b = Client.objects.create(name='bbbb', email='b@b.com')
        contract_b = Contract.objects.create(client=client_b)
        Event.objects.create(name='bb', contract=contract_b, date='2020-02-20T00:00:00Z')

        client_c = Client.objects.create(name='cccc', email='c@c.com')
        contract_c = Contract.objects.create(client=client_c)
        Event.objects.create(name='cc', contract=contract_c, date='2025-05-25T00:00:00Z')

        # --
        response = api_client_salesperson.get('/events/?date=2020-02-20')
        data = response.json()

        assert len(data) == 1
        assert data[0]['contract'] == contract_b.pk

        response = api_client_salesperson.get('/events/?date__gte=2018-02-20')
        data = response.json()

        assert len(data) == 2
        assert data[0]['contract'] == contract_b.pk
        assert data[1]['contract'] == contract_c.pk
