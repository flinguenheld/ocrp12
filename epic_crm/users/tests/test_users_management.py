import pytest
from django.shortcuts import get_object_or_404
from django.http import Http404

from epic_crm.users.models import User


@pytest.mark.django_db
class TestUserManagement:

    def test_access_forbidden_without_token(self, client):
        response = client.get('/users/')
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_access_forbidden_for_salesperson(self, client_salesperson):

        response = client_salesperson.get('/users/')
        data = response.json()

        assert response.status_code == 403
        assert 'Only managers are authorized' in data['detail']

        response = client_salesperson.get('/users/' + "1", follow=True)
        assert response.status_code == 403

        response = client_salesperson.post('/users/')
        assert response.status_code == 403

        response = client_salesperson.put('/users/')
        assert response.status_code == 403

        response = client_salesperson.delete('/users/' + "1", follow=True)
        assert response.status_code == 403

    def test_access_forbidden_for_technical_support(self, client_technical_support):

        response = client_technical_support.get('/users/')
        data = response.json()

        assert response.status_code == 403
        assert 'Only managers are authorized' in data['detail']

        response = client_technical_support.get('/users/' + "1", follow=True)
        assert response.status_code == 403

        response = client_technical_support.post('/users/')
        assert response.status_code == 403

        response = client_technical_support.put('/users/')
        assert response.status_code == 403

        response = client_technical_support.delete('/users/' + "1", follow=True)
        assert response.status_code == 403

    def test_list_users(self, client_manager):

        response = client_manager.get('/users/')
        data = response.json()

        assert response.status_code == 200
        assert 'email' in data[0]
        assert 'role' in data[0]
        assert 'pk' in data[0]

    def test_create_user(self, client_manager):

        body = {'email': 'user_management@pytest.com',
                'password': 'test01234',
                'first_name': 'test_name',
                'last_name': 'test_last_name',
                'role': 'Salesperson'}

        response = client_manager.post('/users/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['email'] == body['email']
        assert data['first_name'] == body['first_name']
        assert data['last_name'] == body['last_name']
        assert data['role'] == body['role']

    def test_update_user(self, client_manager):

        user_to_update = User.objects.create_user(email='pouet@pouet.com', password='test01234', role='Manager')

        # --
        body = {'email': 'updated@pytest.com',
                'password': 'test012345678',
                'first_name': 'updated first name',
                'last_name': 'updated last name',
                'role': 'Technical support'}

        response = client_manager.put(f"/users/{user_to_update.pk}/", data=body)
        data = response.json()

        assert response.status_code == 200
        assert data['email'] == body['email']
        assert data['first_name'] == body['first_name']
        assert data['last_name'] == body['last_name']
        assert data['role'] == body['role']

    def test_details_user(self, client_manager):

        user_to_detail = User.objects.create_user(email='pouet@pouet.com',
                                                  password='test01234',
                                                  first_name='Michel',
                                                  last_name='Pinchon',
                                                  role='Technical support')

        # --
        response = client_manager.get(f"/users/{user_to_detail.pk}/")
        data = response.json()

        assert response.status_code == 200
        assert data['email'] == 'pouet@pouet.com'
        assert data['first_name'] == 'Michel'
        assert data['last_name'] == 'Pinchon'
        assert data['role'] == 'Technical support'

    def test_delete_user(self, client_manager):

        user_to_delete = User.objects.create_user(email='pouet@pouet.com', password='test01234', role='Manager')

        # --
        response = client_manager.delete(f"/users/{user_to_delete.pk}/")

        assert response.status_code == 204
        assert User.objects.filter(pk=user_to_delete.pk).count() == 0
