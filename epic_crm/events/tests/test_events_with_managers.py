import pytest

from epic_crm.users.models import User
from epic_crm.clients.models import Client
from epic_crm.contracts.models import Contract
from epic_crm.events.models import Event


@pytest.mark.django_db
class TestEventstWithManagers:

    def test_access_forbiden_without_token(self, client):
        response = client.get('/events/')
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_manager_can_list_events(self, api_client_manager):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        contract_0 = Contract.objects.create(client=client_0, amount=1000)
        Event.objects.create(name='Event name', date='2015-05-15T00:00:00Z', contract=contract_0)

        # --
        response = api_client_manager.get('/events/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['name'] == 'Event name'
        assert data[0]['date'] == '2015-05-15T00:00:00Z'
        assert data[0]['contract'] == contract_0.pk

    def test_manager_can_get_contract_details(self, api_client_manager):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        contract_0 = Contract.objects.create(client=client_0, amount=1000, date_signed='2015-05-15T00:00:00Z')
        event_0 = Event.objects.create(name='Event name', date='2015-05-15T00:00:00Z', contract=contract_0)

        # --
        response = api_client_manager.get(f'/events/{event_0.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'Event name'
        assert data['date'] == '2015-05-15T00:00:00Z'
        assert data['contract']['pk'] == contract_0.pk

    def test_manager_can_create_a_new_event(self, api_client_manager):

        client = Client.objects.create(name='Client name', salesperson=None)
        technical_support = User.objects.create_user(email='t1@test.com', password='0000', role='Technical support')
        contract = Contract.objects.create(client=client, amount=1000, date_signed='2015-05-15T00:00:00Z')

        # --
        body = {'name': 'Fantastic event',
                'date': '2015-05-15',
                'informations': 'Blabla',
                'contract': contract.pk,
                'technical_support': technical_support.pk}

        response = api_client_manager.post('/events/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['name'] == 'Fantastic event'
        assert data['date'] == '2015-05-15T00:00:00Z'
        assert data['contract'] == contract.pk
        assert data['technical_support'] == technical_support.pk

    def test_manager_cannot_create_a_new_event_with_a_contract_which_already_has_an_event(self, api_client_manager):

        client = Client.objects.create(name='Client name', salesperson=None)
        technical_support = User.objects.create_user(email='t1@test.com', password='0000', role='Technical support')
        contract = Contract.objects.create(client=client, amount=1000, date_signed='2015-05-15T00:00:00Z')
        event = Event.objects.create(name='Event name', date='2015-05-15T00:00:00Z', contract=contract)

        # --
        body = {'name': 'Fantastic event',
                'date': '2015-05-15',
                'informations': 'Blabla',
                'contract': contract.pk,
                'technical_support': technical_support.pk}

        response = api_client_manager.post('/events/', data=body)
        data = response.json()

        assert response.status_code == 400
        assert 'event with this contract already exists.' in data['contract']

    def test_manager_can_update_an_event(self, api_client_manager):

        client = Client.objects.create(name='Client name', salesperson=None)
        technical_support = User.objects.create_user(email='t1@test.com', password='0000', role='Technical support')
        contract = Contract.objects.create(client=client, amount=1000, date_signed='2015-05-15T00:00:00Z')

        event_to_update = Event.objects.create(name='Event name',
                                               date='2015-05-15T00:00:00Z',
                                               contract=contract)

        # --
        body = {'name': 'Fantastic event',
                'date': '2020-10-20T00:00:00Z',
                'informations': 'Blabla',
                'contract': contract.pk,
                'technical_support': technical_support.pk}

        response = api_client_manager.put(f'/events/{event_to_update.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == 'Fantastic event'
        assert data['date'] == '2020-10-20T00:00:00Z'
        assert data['informations'] == 'Blabla'
        assert data['technical_support'] == technical_support.pk

    def test_manager_cannot_assign_a_non_technical_support_user_to_an_event(self, api_client_manager):

        client = Client.objects.create(name='Client name', salesperson=None)
        contract = Contract.objects.create(client=client, amount=1000, date_signed='2015-05-15T00:00:00Z')

        salesperson = User.objects.create_user(email='s0@test.com', password='0000', role='Salesperson')
        event_to_update = Event.objects.create(name='Event name',
                                               date='2015-05-15T00:00:00Z',
                                               contract=contract)

        # --
        body = {'name': 'Fantastic event',
                'date': '2020-10-20T00:00:00Z',
                'informations': 'Blabla',
                'technical_support': salesperson.pk}

        response = api_client_manager.put(f'/events/{event_to_update.pk}/', data=body)
        data = response.json()

        assert response.status_code == 400
        assert "Only users with the role 'Technical support' are valid" in data['technical_support']

    def test_manager_can_delete_an_event(self, api_client_manager):

        client = Client.objects.create(name='Client name', salesperson=None)
        contract = Contract.objects.create(client=client, amount=1000, date_signed='2015-05-15T00:00:00Z')

        event_to_delete = Event.objects.create(name='Event name',
                                               date='2015-05-15T00:00:00Z',
                                               contract=contract)
        # --
        response = api_client_manager.delete(f"/events/{event_to_delete.pk}/")

        assert response.status_code == 204
        assert Event.objects.filter(pk=event_to_delete.pk).count() == 0
