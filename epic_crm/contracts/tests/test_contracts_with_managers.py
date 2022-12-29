import pytest

from epic_crm.users.models import User
from epic_crm.clients.models import Client
from epic_crm.contracts.models import Contract


@pytest.mark.django_db
class TestContractWithManagers:

    def test_access_forbiden_without_token(self, client):
        response = client.get('/contracts/')
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_manager_can_list_contracts(self, client_manager):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        contract_0 = Contract.objects.create(client=client_0, amount=1000)

        # --
        response = client_manager.get('/contracts/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['client'] == contract_0.client.pk
        assert data[0]['amount'] == 1000

    def test_manager_can_get_contract_details(self, client_manager):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        contract_0 = Contract.objects.create(client=client_0, amount=1000, date_signed='2015-05-15T00:00:00Z')

        # --
        response = client_manager.get(f'/contracts/{contract_0.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['amount'] == 1000
        assert data['date_signed'] == '2015-05-15T00:00:00Z'
        assert data['client']['pk'] == contract_0.client.pk
        assert data['client']['name'] == contract_0.client.name

    def test_manager_can_create_a_new_contract(self, client_manager):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        salesperson_0 = User.objects.create_user(email='s0@test.com', password='0000', role='Salesperson')

        # --
        body = {'signatory': salesperson_0.pk,
                'date_signed': '2015-05-15',
                'client': client_0.pk,
                'amount': 3000}

        response = client_manager.post('/contracts/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['signatory'] == salesperson_0.pk
        assert data['date_signed'] == '2015-05-15T00:00:00Z'
        assert data['client'] == client_0.pk
        assert data['amount'] == 3000

    def test_manager_can_update_a_contract(self, client_manager):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        client_1 = Client.objects.create(name='Client name 1', salesperson=None)
        salesperson_0 = User.objects.create_user(email='s0@test.com', password='0000', role='Salesperson')
        contract_to_update = Contract.objects.create(client=client_0, amount=1000, date_signed='2022-01-22T00:00:00Z')

        # --
        body = {'signatory': salesperson_0.pk,
                'date_signed': '2015-05-15',
                'client': client_1.pk,
                'amount': 555.55}

        response = client_manager.put(f'/contracts/{contract_to_update.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['signatory'] == salesperson_0.pk
        assert data['date_signed'] == '2015-05-15T00:00:00Z'
        assert data['client'] == client_1.pk
        assert data['amount'] == 555.55

    def test_manager_cannot_assign_a_non_salesperson_user_to_a_contract(self, client_manager):

        client = Client.objects.create(name='Client name', salesperson=None)
        contract_to_update = Contract.objects.create(client=client, amount=1000, date_signed='2022-01-22T00:00:00Z')
        technical_support = User.objects.create_user(email='t1@test.com', password='0000', role='Technical support')

        # --
        body = {'signatory': technical_support.pk,
                'date_signed': '2015-05-15',
                'client': client.pk,
                'amount': 555.55}

        response = client_manager.put(f"/contracts/{contract_to_update.pk}/", data=body)
        data = response.json()

        assert response.status_code == 400
        assert "Only users with the role 'Salesperson' are valid" in data['signatory']

    def test_manager_can_delete_a_contract(self, client_manager):

        client = Client.objects.create(name='Client name', salesperson=None)
        contract_to_delete = Contract.objects.create(client=client, amount=1000, date_signed='2022-01-22T00:00:00Z')

        # --
        response = client_manager.delete(f"/contracts/{contract_to_delete.pk}/")

        assert response.status_code == 204
        assert Client.objects.filter(pk=contract_to_delete.pk).count() == 0
