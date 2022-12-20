import pytest
import requests
from random import randint

"""
    These tests need three users :
        manager@pytest.com
        salesperson@pytest.com
        technical_support@pytest.com

        With the same password : test01234
"""


# Variable shared between tests (impossible without pytest hook)
def pytest_namespace():
    return {'pk_new_client': -1,
            'pk_manager': -1}


def connect_user(email, password='test01234'):

    response_login = requests.post("http://localhost:8000/login/", json={"email": email, "password": password})
    data = response_login.json()

    return f"Bearer {data['access']}" if 'access' in data else ""


class TestClientManagement:

    token_manager = connect_user('manager@pytest.com')
    token_salesperson = connect_user('salesperson@pytest.com')
    token_salesperson_2 = connect_user('salesperson_2@pytest.com')
    token_technical_support = connect_user('technical_support@pytest.com')

    ENDPOINT = "http://localhost:8000/clients/"
    random_number = randint(0, 1000000)

    def test_access_forbiden_without_token(self):
        response = requests.get(self.ENDPOINT)
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_salesperson_can_create_a_new_client(self):

        body = {'name': f'Test client created by salesperson {self.random_number}',
                'address': '40 rue du lac 37000 Tours',
                'email': 'hello@test.com',
                'phone': '0600000000'}

        response = requests.post(self.ENDPOINT,
                                 json=body,
                                 headers={"Authorization": self.token_salesperson})
        data = response.json()

        assert response.status_code == 201
        assert data['name'] == body['name']
        assert data['address'] == body['address']
        assert data['email'] == body['email']
        assert data['phone'] == body['phone']

        pytest.pk_new_client = str(data['pk'])

    def test_assigned_salesperson_can_update_the_new_client(self):

        body = {'name': f'Test client updated by salesperson {self.random_number}',
                'address': '40 rue du lac 37000 Tours updated',
                'email': 'hello_updated@test.com',
                'phone': '0611111111'}

        response_salesperson = requests.put(self.ENDPOINT + pytest.pk_new_client + '/',
                                            json=body,
                                            headers={"Authorization": self.token_salesperson})
        data_salesperson = response_salesperson.json()

        assert response_salesperson.status_code == 200
        assert data_salesperson['name'] == body['name']
        assert data_salesperson['address'] == body['address']

    def test_manager_can_update_the_new_client(self):

        body = {'name': f'Test client updated by manager {self.random_number}',
                'address': '40 rue du lac 37000 Tours updated twice',
                'email': 'hello_updated_twice@test.com',
                'phone': '0622222222'}

        response_salesperson = requests.put(self.ENDPOINT + pytest.pk_new_client + '/',
                                            json=body,
                                            headers={"Authorization": self.token_manager})
        data_salesperson = response_salesperson.json()

        assert response_salesperson.status_code == 200
        assert data_salesperson['name'] == body['name']
        assert data_salesperson['address'] == body['address']

    def test_another_salesperson_can_get_the_new_client(self):

        response = requests.get(self.ENDPOINT, headers={"Authorization": self.token_salesperson_2})
        data = response.json()

        assert response.status_code == 200
        assert any([True for v in data if int(pytest.pk_new_client) == v['pk']])

        # Details --
        response_details = requests.get(self.ENDPOINT + pytest.pk_new_client + '/',
                                        headers={"Authorization": self.token_salesperson_2})
        data = response_details.json()

        assert response_details.status_code == 200
        assert 'hello_updated_twice' in data['email']

    def test_however_another_saleperson_cannot_update_the_new_client(self):

        body = {'name': f'Test client updated by another salesperson {self.random_number}',
                'address': '40 rue du lac 37000 Tours updated',
                'email': 'hello_updated@test.com',
                'phone': '0611111111'}

        response_create = requests.put(self.ENDPOINT + pytest.pk_new_client + '/',
                                       json=body,
                                       headers={"Authorization": self.token_salesperson_2})
        data = response_create.json()

        assert response_create.status_code == 403
        assert "Only the assigned salesperson or managers are authorized" in data['detail']

    def test_technical_support_can_get_the_new_client(self):

        response = requests.get(self.ENDPOINT, headers={"Authorization": self.token_technical_support})
        data = response.json()

        assert response.status_code == 200
        assert any([True for v in data if int(pytest.pk_new_client) == v['pk']])

        # Details --
        response_details = requests.get(self.ENDPOINT + pytest.pk_new_client + '/',
                                        headers={"Authorization": self.token_technical_support})
        data = response_details.json()

        assert response_details.status_code == 200
        assert 'hello_updated_twice' in data['email']

    def test_however_technical_support_cannot_update_the_new_client(self):

        body = {'name': f'Test client updated by another salesperson {self.random_number}',
                'address': '40 rue du lac 37000 Tours updated',
                'email': 'hello_updated@test.com',
                'phone': '0611111111'}

        response_create = requests.put(self.ENDPOINT + pytest.pk_new_client + '/',
                                       json=body,
                                       headers={"Authorization": self.token_technical_support})
        data = response_create.json()

        assert response_create.status_code == 403
        assert "Only the assigned salesperson or managers are authorized" in data['detail']

    def test_manager_can_create_a_new_client(self):

        body = {'name': f'Test client created by manager {self.random_number}',
                'address': '40 rue du lac 37000 Tours',
                'email': 'hello@test.com',
                'phone': '0600000000'}

        response_create = requests.post(self.ENDPOINT,
                                        json=body,
                                        headers={"Authorization": self.token_manager})
        data = response_create.json()

        assert response_create.status_code == 201
        assert data['name'] == body['name']
        assert data['salesperson'] is None

    def test_manager_cannot_assign_a_non_salesperson_user_to_the_client(self):

        response = requests.get("http://localhost:8000/users/", headers={"Authorization": self.token_manager})
        data = response.json()

        for user in data:
            if user['role'] == 'Manager':
                pytest.pk_manager = str(user['pk'])

        body = {'name': f'Test client updated by manager {self.random_number}',
                'address': '40 rue du lac 37000 Tours updated thrice',
                'email': 'hello_updated_thrice@test.com',
                'phone': '0622222222',
                'salesperson': pytest.pk_manager}

        response_salesperson = requests.put(self.ENDPOINT + pytest.pk_new_client + '/',
                                            json=body,
                                            headers={"Authorization": self.token_manager})
        data_salesperson = response_salesperson.json()

        assert response_salesperson.status_code == 400
        assert "Only users with the role 'Salesperson' are valid" in data_salesperson['salesperson']
