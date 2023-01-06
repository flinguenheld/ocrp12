import pytest

from django.contrib.auth.models import User
from epic_crm.users.models import UserRole
from epic_crm.clients.models import Client
from epic_crm.contracts.models import Contract
from epic_crm.events.models import Event


@pytest.mark.django_db
class TestEventsWithTechnicalSupports:

    def test_technical_support_can_list_events(self, api_client_technical_support):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        contract_0 = Contract.objects.create(client=client_0, amount=1000)
        Event.objects.create(name='Event name', date='2015-05-15T00:00:00Z', contract=contract_0)

        # --
        response = api_client_technical_support.get('/events/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['name'] == 'Event name'
        assert data[0]['date'] == '2015-05-15T00:00:00Z'
        assert data[0]['contract'] == contract_0.pk

    def test_salesperson_can_get_client_details(self, api_client_technical_support):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        contract_0 = Contract.objects.create(client=client_0, amount=1000, date_signed='2015-05-15T00:00:00Z')
        event_0 = Event.objects.create(name='Event name', date='2015-05-15T00:00:00Z', contract=contract_0)

        # --
        response = api_client_technical_support.get(f'/events/{event_0.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'Event name'
        assert data['date'] == '2015-05-15T00:00:00Z'
        assert data['contract']['pk'] == contract_0.pk

    def test_technical_support_cannot_create_a_new_event(self, api_client_technical_support):

        salesperson = UserEpic.objects.create_user(email='as@test.com', password='0000', role='Salesperson')
        client = Client.objects.create(name='Client name', salesperson=salesperson)
        contract = Contract.objects.create(client=client, amount=1000, date_signed='2015-05-15T00:00:00Z')

        # --
        body = {'name': 'Fantastic event',
                'date': '2015-05-15',
                'informations': 'Blabla',
                'contract': contract.pk}

        response = api_client_technical_support.post('/events/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the client assigned salesperson or managers are authorized to do this request' in data['detail']

    def test_assigned_technical_support_can_update_an_event(self, api_client_technical_support):

        technical_support = UserEpic.objects.get(email='technical_support@pytest.com')

        salesperson = UserEpic.objects.create_user(email='as@test.com', password='0000', role='Salesperson')
        client = Client.objects.create(name='Client name', salesperson=salesperson)
        contract = Contract.objects.create(client=client, amount=1000, date_signed='2015-05-15T00:00:00Z')

        event_to_update = Event.objects.create(name='Event name',
                                               date='2015-05-15T00:00:00Z',
                                               contract=contract,
                                               technical_support=technical_support)

        # --
        body = {'name': 'Fantastic event',
                'date': '2020-10-20T00:00:00Z',
                'informations': 'Blabla'}

        response = api_client_technical_support.put(f'/events/{event_to_update.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'Fantastic event'
        assert data['date'] == '2020-10-20T00:00:00Z'
        assert data['informations'] == 'Blabla'

    def test_non_assigned_technical_support_cannot_update_an_event(self, api_client_technical_support):

        another_technical_support = UserEpic.objects.create_user(email='ats@test.com',
                                                             password='0000',
                                                             role='Technical support')

        salesperson = UserEpic.objects.create_user(email='as@test.com', password='0000', role='Salesperson')
        client = Client.objects.create(name='Client name', salesperson=salesperson)
        contract = Contract.objects.create(client=client, amount=1000, date_signed='2015-05-15T00:00:00Z')

        event_to_update = Event.objects.create(name='Event name',
                                               date='2015-05-15T00:00:00Z',
                                               contract=contract,
                                               technical_support=another_technical_support)

        # --
        body = {'name': 'Fantastic event',
                'date': '2020-10-20T00:00:00Z',
                'informations': 'Blabla'}

        response = api_client_technical_support.put(f'/events/{event_to_update.pk}/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the client assigned salesperson or managers are authorized to do this request' in data['detail']

    def test_technical_support_cannot_delete_an_event(self, api_client_technical_support):

        technical_support = UserEpic.objects.get(email='technical_support@pytest.com')
        salesperson = UserEpic.objects.create_user(email='as@test.com', password='0000', role='Salesperson')
        client = Client.objects.create(name='Client name', salesperson=salesperson)
        contract = Contract.objects.create(client=client, amount=1000, date_signed='2015-05-15T00:00:00Z')

        event_to_delete = Event.objects.create(name='Event name',
                                               date='2015-05-15T00:00:00Z',
                                               contract=contract,
                                               technical_support=technical_support)

        # --
        response = api_client_technical_support.delete(f'/events/{event_to_delete.pk}/')
        data = response.json()

        assert response.status_code == 403
        assert 'Only managers are authorized to do this request' in data['detail']
