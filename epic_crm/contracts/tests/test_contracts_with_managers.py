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
        contract_0 = Contract.objects.create(client=client_0)

        # --
        response = client_manager.get('/contracts/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['client'] == contract_0.client.pk

    def test_manager_can_get_contract_details(self, client_manager):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        contract_0 = Contract.objects.create(client=client_0)

        # --
        response = client_manager.get(f'/contracts/{contract_0.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['client']['pk'] == contract_0.client.pk
        assert data['client']['name'] == contract_0.client.name

    def test_manager_can_create_a_new_contract(self, client_manager):

        client_0 = Client.objects.create(name='Client name', salesperson=None)
        salesperson_0 = User.objects.create_user(email='s0@test.com', password='0000', role='Salesperson')

        # --
        body = {'signatory': salesperson_0.pk,
                # 'date_signed': ,
                'client': client_0.pk}

        response = client_manager.post('/contracts/', data=body)
        data = response.json()

        print(data)
        assert response.status_code == 201
        assert data['signatory'] == salesperson_0.pk
        assert data['client'] == client_0.pk

    # def test_manager_can_update_a_client(self, client_manager):

        # salesperson_1 = User.objects.create_user(email='s1@test.com', password='0000', role='Salesperson')
        # salesperson_2 = User.objects.create_user(email='s2@test.com', password='0000', role='Salesperson')
        # technical_support_1 = User.objects.create_user(email='t1@test.com', password='0000', role='Technical support')

        # client_to_update = Client.objects.create(name='Client name',
                                                 # address='40 rue du lac 37000 Tours',
                                                 # email='hello@test.com',
                                                 # phone='0600000000',
                                                 # salesperson=salesperson_1)
        # # --
        # body = {'name': 'Client name updated',
                # 'address': '10 rue du lac 37000 Tours',
                # 'email': 'updated@test.com',
                # 'phone': '0611111111',
                # 'salesperson': salesperson_2.pk}

        # response = client_manager.put(f"/clients/{client_to_update.pk}/", data=body)
        # data = response.json()

        # assert response.status_code == 200
        # assert data['name'] == body['name']
        # assert data['salesperson'] == salesperson_2.pk

    # def test_manager_cannot_assign_a_non_salesperson_user_to_a_client(self, client_manager):

        # salesperson_1 = User.objects.create_user(email='s1@test.com', password='0000', role='Salesperson')
        # technical_support_1 = User.objects.create_user(email='t1@test.com', password='0000', role='Technical support')

        # client_to_update = Client.objects.create(name='Client name',
                                                 # address='40 rue du lac 37000 Tours',
                                                 # email='hello@test.com',
                                                 # phone='0600000000',
                                                 # salesperson=salesperson_1)
        # # --
        # body = {'name': 'Client name updated',
                # 'address': '10 rue du lac 37000 Tours',
                # 'email': 'updated@test.com',
                # 'phone': '0611111111',
                # 'salesperson': technical_support_1.pk}

        # response = client_manager.put(f"/clients/{client_to_update.pk}/", data=body)
        # data = response.json()

        # assert response.status_code == 400
        # assert "Only users with the role 'Salesperson' are valid" in data['salesperson']

    # def test_manager_can_delete_a_client(self, client_manager):

        # client_to_delete = Client.objects.create(name='Client name')

        # # --
        # response = client_manager.delete(f"/clients/{client_to_delete.pk}/")

        # assert response.status_code == 204
        # assert Client.objects.filter(pk=client_to_delete.pk).count() == 0
