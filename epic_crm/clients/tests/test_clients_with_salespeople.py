import pytest

from epic_crm.users.models import User
from epic_crm.clients.models import Client


@pytest.mark.django_db
class TestClientsWithSalespeople:

    def test_salesperson_can_list_clients(self, api_client_salesperson):

        client_0 = Client.objects.create(name='Client name',
                                         salesperson=None)

        # --
        response = api_client_salesperson.get('/clients/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['name'] == client_0.name

    def test_salesperson_can_get_client_details(self, api_client_salesperson):

        client_0 = Client.objects.create(name='Client name',
                                         salesperson=None)

        # --
        response = api_client_salesperson.get(f'/clients/{client_0.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == client_0.name

    def test_salesperson_can_create_a_new_client(self, api_client_salesperson):

        body = {'name': 'Client name',
                'address': '40 rue du lac 37000 Tours',
                'email': 'hello@test.com',
                'phone': '0600000000'}

        response = api_client_salesperson.post('/clients/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['name'] == body['name']
        assert data['address'] == body['address']
        assert data['email'] == body['email']
        assert data['phone'] == body['phone']

    def test_assigned_salesperson_can_update_his_client(self, api_client_salesperson):

        # Get the user then create a client with him as salesperson
        user = User.objects.get(email='salesperson@pytest.com')
        client_to_update = Client.objects.create(name='Client name',
                                                 address='40 rue du lac 37000 Tours',
                                                 email='hello@test.com',
                                                 phone='0600000000',
                                                 salesperson=user)
        # --
        body = {'name': 'Client name updated',
                'address': '10 rue du lac 37000 Tours',
                'email': 'updated@test.com',
                'phone': '0611111111'}

        response = api_client_salesperson.put(f"/clients/{client_to_update.pk}/", data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == body['name']
        assert data['address'] == body['address']
        assert data['email'] == body['email']
        assert data['phone'] == body['phone']

        # Salespeople do not have access to this field (Only manager)
        assert 'salesperson' not in data

    def test_non_assigned_salesperson_cannot_update_a_client(self, api_client_salesperson):

        salesperson_1 = User.objects.create_user(email='s1@test.com', password='0000', role='Salesperson')
        client_to_update = Client.objects.create(name='Client name',
                                                 address='40 rue du lac 37000 Tours',
                                                 email='hello@test.com',
                                                 phone='0600000000',
                                                 salesperson=salesperson_1)
        # --
        body = {'name': 'Client name updated',
                'address': '10 rue du lac 37000 Tours',
                'email': 'updated@test.com',
                'phone': '0611111111'}

        response = api_client_salesperson.put(f"/clients/{client_to_update.pk}/", data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the assigned salesperson or managers are authorized to do this request' in data['detail']

    def test_salesperson_cannot_delete_a_client(self, api_client_salesperson):

        client_to_delete = Client.objects.create(name='Client name')

        # --
        response = api_client_salesperson.delete(f"/clients/{client_to_delete.pk}/")
        data = response.json()

        assert response.status_code == 403
        assert 'Only managers are authorized to do this request' in data['detail']
