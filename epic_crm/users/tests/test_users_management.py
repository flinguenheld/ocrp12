import pytest
import requests

"""
    These tests need three users :
        manager@pytest.com
        salesperson@pytest.com
        technical_support@pytest.com

        With the same password : test01234
"""


# Variable shared between tests (impossible without pytest hook)
def pytest_namespace():
    return {'pk_test_user': -1}


def connect_user(email, password='test01234'):

    response_login = requests.post("http://localhost:8000/login/", json={"email": email, "password": password})
    data = response_login.json()

    return f"Bearer {data['access']}" if 'access' in data else ""


class TestUserManagement:

    token_manager = connect_user('manager@pytest.com')
    token_salesperson = connect_user('salesperson@pytest.com')
    token_technical_support = connect_user('technical_support@pytest.com')

    ENDPOINT = "http://localhost:8000/users/"

    def test_access_forbidden_without_token(self):
        response = requests.get(self.ENDPOINT)
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_access_forbidden_for_salesperson(self):
        response = requests.get(self.ENDPOINT, headers={"Authorization": self.token_salesperson})
        data = response.json()

        assert response.status_code == 403
        assert 'Only managers are authorized' in data['detail']

        response = requests.get(self.ENDPOINT + "1", headers={"Authorization": self.token_salesperson})
        assert response.status_code == 403

        response = requests.post(self.ENDPOINT, headers={"Authorization": self.token_salesperson})
        assert response.status_code == 403

        response = requests.put(self.ENDPOINT, headers={"Authorization": self.token_salesperson})
        assert response.status_code == 403

        response = requests.delete(self.ENDPOINT + "1", headers={"Authorization": self.token_salesperson})
        assert response.status_code == 403

    def test_access_forbidden_for_technical_support(self):
        response = requests.get(self.ENDPOINT, headers={"Authorization": self.token_technical_support})
        data = response.json()

        assert response.status_code == 403
        assert 'Only managers are authorized' in data['detail']

        response = requests.get(self.ENDPOINT + "1", headers={"Authorization": self.token_technical_support})
        assert response.status_code == 403

        response = requests.post(self.ENDPOINT, headers={"Authorization": self.token_technical_support})
        assert response.status_code == 403

        response = requests.put(self.ENDPOINT, headers={"Authorization": self.token_technical_support})
        assert response.status_code == 403

        response = requests.delete(self.ENDPOINT + "1", headers={"Authorization": self.token_technical_support})
        assert response.status_code == 403

    def test_list_users(self):

        response = requests.get(self.ENDPOINT, headers={"Authorization": self.token_manager})
        data = response.json()

        assert response.status_code == 200
        assert 'email' in data[0]
        assert 'role' in data[0]
        assert 'pk' in data[0]

    def test_create_user(self):

        body = {'email': 'user_management@pytest.com',
                'password': 'test01234',
                'first_name': 'test_name',
                'last_name': 'test_last_name',
                'role': 'Salesperson'}

        response_create = requests.post(self.ENDPOINT,
                                        json=body,
                                        headers={"Authorization": self.token_manager})

        data = response_create.json()
        pytest.pk_test_user = str(data['pk'])

        assert response_create.status_code == 201
        assert data['email'] == body['email']
        # assert data['password'] == body['password']
        assert data['first_name'] == body['first_name']
        assert data['last_name'] == body['last_name']
        assert data['role'] == body['role']

    def test_update_user(self):

        body = {'email': 'user_management_updated@pytest.com',
                'password': 'test012345678',
                'first_name': 'test_name_updated',
                'last_name': 'test_last_name_updated',
                'role': 'Manager'}

        response_create = requests.put(self.ENDPOINT + pytest.pk_test_user + "/",
                                       json=body,
                                       headers={"Authorization": self.token_manager})

        data = response_create.json()

        assert response_create.status_code == 200
        assert data['email'] == body['email']
        # assert data['password'] == body['password']
        assert data['first_name'] == body['first_name']
        assert data['last_name'] == body['last_name']
        assert data['role'] == body['role']

    def test_details_user(self):

        response_create = requests.get(self.ENDPOINT + pytest.pk_test_user + "/",
                                       headers={"Authorization": self.token_manager})

        data = response_create.json()

        assert response_create.status_code == 200
        assert data['email'] == 'user_management_updated@pytest.com'
        assert data['first_name'] == 'test_name_updated'
        assert data['last_name'] == 'test_last_name_updated'
        assert data['role'] == 'Manager'

    def test_delete_user(self):

        response = requests.delete(self.ENDPOINT + pytest.pk_test_user + "/",
                                   headers={"Authorization": self.token_manager})

        assert response.status_code == 204
