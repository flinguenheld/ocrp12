import pytest

from epic_crm.users.models import User
from epic_crm.clients.models import Client


@pytest.mark.django_db
class TestClientWithSalespeople:

    def test_technical_support_can_list_clients(self, client_technical_support):

        client_0 = Client.objects.create(name='Client name',
                                         salesperson=None)

        # --
        response = client_technical_support.get('/clients/')
        data = response.json()

        assert response.status_code == 200
        assert data[0]['name'] == client_0.name

    def test_technical_support_can_get_client_details(self, client_technical_support):

        client_0 = Client.objects.create(name='Client name',
                                         salesperson=None)

        # --
        response = client_technical_support.get(f'/clients/{client_0.pk}/')
        data = response.json()

        assert response.status_code == 200
        assert data['name'] == client_0.name

    def test_technical_support_cannot_create_a_new_client(self, client_technical_support):

        salseperson = User.objects.create_user(email='aa@aa.com', password='pass', role='Salesperson')

        # --
        body = {'name': 'Client name',
                'address': '40 rue du lac 37000 Tours',
                'email': 'hello@test.com',
                'phone': '0600000000',
                'salesperson': salseperson}

        response = client_technical_support.post('/clients/', data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only salespeople or managers are authorized to do this request' in data['detail']

    def test_technical_support_cannot_update_a_client(self, client_technical_support):

        client_to_update = Client.objects.create(name='Client name',
                                                 address='40 rue du lac 37000 Tours',
                                                 email='hello@test.com',
                                                 phone='0600000000',
                                                 salesperson=None)
        # --
        body = {'name': 'Client name updated',
                'address': '10 rue du lac 37000 Tours',
                'email': 'updated@test.com',
                'phone': '0611111111'}

        response = client_technical_support.put(f"/clients/{client_to_update.pk}/", data=body)
        data = response.json()

        assert response.status_code == 403
        assert 'Only the assigned salesperson or managers are authorized to do this request' in data['detail']
