import pytest

from epic_crm.users.models import User
from epic_crm.clients.models import Client
from epic_crm.contracts.models import Contract


@pytest.mark.django_db
class TestClientWithSalespeople:

    def test_salesperson_can_list_contracts(self, client_salesperson):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        contract_0 = Contract.objects.create(client=client_0, amount=1000, date_signed='2015-05-15T00:00:00Z')

        # --
        response = client_salesperson.get('/contracts/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['client'] == contract_0.client.pk
        assert data[0]['amount'] == 1000

    def test_salesperson_can_get_client_details(self, client_salesperson):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        contract_0 = Contract.objects.create(client=client_0, amount=1000)

        # --
        response = client_salesperson.get('/contracts/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['client'] == contract_0.client.pk
        assert data[0]['amount'] == 1000

    def test_assigned_salesperson_can_create_a_new_contract(self, client_salesperson):

        salesperson = User.objects.get(email='salesperson@pytest.com')
        client = Client.objects.create(name='Client name', salesperson=salesperson)

        # --
        body = {'date_signed': '2015-05-15',
                'client': client.pk,
                'amount': 1000}

        response = client_salesperson.post('/contracts/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['amount'] == 1000.0

        created_contract = Contract.objects.get(pk=data['pk'])

        assert created_contract.client.pk == client.pk
        assert created_contract.signatory.pk == salesperson.pk  # not in the serializer, it has to be auto completed

    def test_non_assigned_salesperson_cannot_create_a_new_contract(self, client_salesperson):

        another_salesperson = User.objects.create_user(email='as@test.com', password='0000', role='Salesperson')
        client_assigned_to_another_salesperson = Client.objects.create(name='Client name',
                                                                       salesperson=another_salesperson)

        # --
        body = {'date_signed': '2015-05-15',
                'client': client_assigned_to_another_salesperson.pk,
                'amount': 1000}

        response = client_salesperson.post('/contracts/', data=body)
        data = response.json()

        assert response.status_code == 400
        assert 'Only the assigned salesperson and managers are authorized to create a contract' in data

    def test_assigned_salesperson_can_update_a_contract(self, client_salesperson):

        salesperson = User.objects.get(email='salesperson@pytest.com')
        client = Client.objects.create(name='Client name', salesperson=salesperson)
        contract_to_update = Contract.objects.create(client=client, amount=1000, date_signed='2022-01-22T00:00:00Z')

        # --
        body = {'date_signed': '2015-05-15',
                'amount': 555.55}

        response = client_salesperson.put(f'/contracts/{contract_to_update.pk}/', data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['date_signed'] == '2015-05-15T00:00:00Z'
        assert data['amount'] == 555.55

    def test_non_assigned_salesperson_cannot_update_a_contract(self, client_salesperson):

        another_salesperson = User.objects.create_user(email='as@test.com', password='0000', role='Salesperson')
        client_assigned_to_another_salesperson = Client.objects.create(name='Client name',
                                                                       salesperson=another_salesperson)
        contract_to_update = Contract.objects.create(client=client_assigned_to_another_salesperson,
                                                     amount=1000,
                                                     date_signed='2022-01-22T00:00:00Z')

        # --
        body = {'date_signed': '2015-05-15',
                'client': client_assigned_to_another_salesperson.pk,
                'amount': 1000}

        response = client_salesperson.put(f'/contracts/{contract_to_update.pk}/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the assigned salesperson or managers are authorized to do this request' in data['detail']

    def test_salesperson_cannot_delete_a_contract(self, client_salesperson):

        salesperson = User.objects.get(email='salesperson@pytest.com')
        client = Client.objects.create(name='Client name', salesperson=salesperson)
        contract_to_delete = Contract.objects.create(client=client, amount=1000, date_signed='2022-01-22T00:00:00Z')

        # --
        response = client_salesperson.delete(f'/contracts/{contract_to_delete.pk}/')
        data = response.json()

        assert response.status_code == 403
        assert 'Only managers are authorized to do this request' in data['detail']
