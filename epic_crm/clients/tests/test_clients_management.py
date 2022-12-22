import pytest
from random import randint

from epic_crm.clients.models import Client


@pytest.mark.django_db
class TestClientManagement:

    def test_access_forbiden_without_token(self, client):
        response = client.get('/clients/')
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_salesperson_can_create_a_new_client(self, client_salesperson):

        body = {'name': 'Client name',
                'address': '40 rue du lac 37000 Tours',
                'email': 'hello@test.com',
                'phone': '0600000000'}

        response = client_salesperson.post('/clients/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['name'] == body['name']
        assert data['address'] == body['address']
        assert data['email'] == body['email']
        assert data['phone'] == body['phone']

    # def test_assigned_salesperson_can_update_client(self, client_salesperson):

        # client_to_update = Client.objects.create(name='Client name',
                                                 # address='40 rue du lac 37000 Tours',
                                                 # email='hello@test.com',
                                                 # phone='0600000000')

        # body = {'name': 'Client name updated',
                # 'address': '10 rue du lac 37000 Tours',
                # 'email': 'updated@test.com',
                # 'phone': '0611111111'}

        # print(client_to_update.pk)
        # response_salesperson = client_salesperson.put(f"/clients/{client_to_update}/", data=body)
        # data = response_salesperson.json()

        # assert response_salesperson.status_code == 200
        # assert data_salesperson['name'] == body['name']
        # assert data_salesperson['address'] == body['address']

    # def test_manager_can_update_client(self):

        # body = {'name': f'Test client updated by manager {self.random_number}',
                # 'address': '40 rue du lac 37000 Tours updated twice',
                # 'email': 'hello_updated_twice@test.com',
                # 'phone': '0622222222'}

        # response_salesperson = requests.put(self.ENDPOINT + pytest.pk_new_client + '/',
                                            # json=body,
                                            # headers={"Authorization": self.token_manager})
        # data_salesperson = response_salesperson.json()

        # assert response_salesperson.status_code == 200
        # assert data_salesperson['name'] == body['name']
        # assert data_salesperson['address'] == body['address']

    # def test_another_salesperson_can_get_the_new_client(self):

        # response = requests.get(self.ENDPOINT, headers={"Authorization": self.token_salesperson_2})
        # data = response.json()

        # assert response.status_code == 200
        # assert any([True for v in data if int(pytest.pk_new_client) == v['pk']])

        # # Details --
        # response_details = requests.get(self.ENDPOINT + pytest.pk_new_client + '/',
                                        # headers={"Authorization": self.token_salesperson_2})
        # data = response_details.json()

        # assert response_details.status_code == 200
        # assert 'hello_updated_twice' in data['email']

    # def test_however_another_saleperson_cannot_update_the_new_client(self):

        # body = {'name': f'Test client updated by another salesperson {self.random_number}',
                # 'address': '40 rue du lac 37000 Tours updated',
                # 'email': 'hello_updated@test.com',
                # 'phone': '0611111111'}

        # response_create = requests.put(self.ENDPOINT + pytest.pk_new_client + '/',
                                       # json=body,
                                       # headers={"Authorization": self.token_salesperson_2})
        # data = response_create.json()

        # assert response_create.status_code == 403
        # assert "Only the assigned salesperson or managers are authorized" in data['detail']

    # def test_technical_support_can_get_the_new_client(self):

        # response = requests.get(self.ENDPOINT, headers={"Authorization": self.token_technical_support})
        # data = response.json()

        # assert response.status_code == 200
        # assert any([True for v in data if int(pytest.pk_new_client) == v['pk']])

        # # Details --
        # response_details = requests.get(self.ENDPOINT + pytest.pk_new_client + '/',
                                        # headers={"Authorization": self.token_technical_support})
        # data = response_details.json()

        # assert response_details.status_code == 200
        # assert 'hello_updated_twice' in data['email']

    # def test_however_technical_support_cannot_update_the_new_client(self):

        # body = {'name': f'Test client updated by another salesperson {self.random_number}',
                # 'address': '40 rue du lac 37000 Tours updated',
                # 'email': 'hello_updated@test.com',
                # 'phone': '0611111111'}

        # response_create = requests.put(self.ENDPOINT + pytest.pk_new_client + '/',
                                       # json=body,
                                       # headers={"Authorization": self.token_technical_support})
        # data = response_create.json()

        # assert response_create.status_code == 403
        # assert "Only the assigned salesperson or managers are authorized" in data['detail']

    # def test_manager_can_create_a_new_client(self):

        # body = {'name': f'Test client created by manager {self.random_number}',
                # 'address': '40 rue du lac 37000 Tours',
                # 'email': 'hello@test.com',
                # 'phone': '0600000000'}

        # response_create = requests.post(self.ENDPOINT,
                                        # json=body,
                                        # headers={"Authorization": self.token_manager})
        # data = response_create.json()

        # assert response_create.status_code == 201
        # assert data['name'] == body['name']
        # assert data['salesperson'] is None

    # def test_manager_cannot_assign_a_non_salesperson_user_to_the_client(self):

        # response = requests.get("http://localhost:8000/users/", headers={"Authorization": self.token_manager})
        # data = response.json()

        # for user in data:
            # if user['role'] == 'Manager':
                # pytest.pk_manager = str(user['pk'])

        # body = {'name': f'Test client updated by manager {self.random_number}',
                # 'address': '40 rue du lac 37000 Tours updated thrice',
                # 'email': 'hello_updated_thrice@test.com',
                # 'phone': '0622222222',
                # 'salesperson': pytest.pk_manager}

        # response_salesperson = requests.put(self.ENDPOINT + pytest.pk_new_client + '/',
                                            # json=body,
                                            # headers={"Authorization": self.token_manager})
        # data_salesperson = response_salesperson.json()

        # assert response_salesperson.status_code == 400
        # assert "Only users with the role 'Salesperson' are valid" in data_salesperson['salesperson']
