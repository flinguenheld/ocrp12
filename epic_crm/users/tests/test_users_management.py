import pytest
from django.shortcuts import get_object_or_404
from django.http import Http404

from django.contrib.auth.models import User
from epic_crm.users.models import UserRole


@pytest.mark.django_db
class TestUserManagement:

    def test_access_forbidden_without_token(self, client):
        response = client.get('/users/')
        data = response.json()

        assert response.status_code == 401
        assert 'Authentication credentials were not provided' in data['detail']

    def test_access_forbidden_for_salesperson(self, api_client_salesperson):

        response = api_client_salesperson.get('/users/')
        data = response.json()

        assert response.status_code == 403
        assert 'Only managers are authorized' in data['detail']

        response = api_client_salesperson.get('/users/' + "1", follow=True)
        assert response.status_code == 403

        response = api_client_salesperson.post('/users/')
        assert response.status_code == 403

        response = api_client_salesperson.put('/users/')
        assert response.status_code == 403

        response = api_client_salesperson.delete('/users/' + "1", follow=True)
        assert response.status_code == 403

    def test_access_forbidden_for_technical_support(self, api_client_technical_support):

        response = api_client_technical_support.get('/users/')
        data = response.json()

        assert response.status_code == 403
        assert 'Only managers are authorized' in data['detail']

        response = api_client_technical_support.get('/users/' + "1", follow=True)
        assert response.status_code == 403

        response = api_client_technical_support.post('/users/')
        assert response.status_code == 403

        response = api_client_technical_support.put('/users/')
        assert response.status_code == 403

        response = api_client_technical_support.delete('/users/' + "1", follow=True)
        assert response.status_code == 403

    def test_list_users(self, api_client_manager):

        response = api_client_manager.get('/users/')
        data = response.json()

        assert response.status_code == 200
        assert 'pk' in data[0]
        assert 'username' in data[0]
        assert 'role_of' in data[0]

    def test_details_user(self, api_client_manager):

        user_to_detail = User.objects.create_user(username='Mirelle',
                                                  email='pouet@pouet.com',
                                                  password='test01234',
                                                  first_name='Michel',
                                                  last_name='Pinchon')

        UserRole.objects.create(user=user_to_detail, role='Salesperson')

        # --
        response = api_client_manager.get(f"/users/{user_to_detail.pk}/")
        data = response.json()

        print(data)
        assert response.status_code == 200
        assert data['username'] == 'Mirelle'
        assert data['email'] == 'pouet@pouet.com'
        assert data['first_name'] == 'Michel'
        assert data['last_name'] == 'Pinchon'
        assert data['role_of']['role'] == 'Salesperson'

    def test_create_user(self, api_client_manager):

        body = {'username': 'user_management',
                'email': 'user_management@pytest.com',
                'password': 'test01234',
                'first_name': 'test_name',
                'last_name': 'test_last_name',
                'role': 'Salesperson'}

        response = api_client_manager.post('/users/', data=body)
        data = response.json()

        assert response.status_code == 201
        assert data['username'] == body['username']
        assert data['email'] == body['email']
        assert data['first_name'] == body['first_name']
        assert data['last_name'] == body['last_name']

        new_user = User.objects.get(username='user_management')
        assert new_user.role_of.role == 'Salesperson'

    def test_update_user(self, api_client_manager):

        user_to_update = User.objects.create_user(username='Mirelle',
                                                  email='pouet@pouet.com',
                                                  password='test01234')

        UserRole.objects.create(user=user_to_update, role='Manager')

        # --
        body = {'username': 'updated_Mirelle',
                'email': 'updated@pytest.com',
                'password': 'test012345678',
                'first_name': 'updated first name',
                'last_name': 'updated last name',
                'role': 'Technical support'}

        response = api_client_manager.put(f"/users/{user_to_update.pk}/", data=body)
        data = response.json()

        assert response.status_code == 200

        updated_user = User.objects.get(pk=user_to_update.pk)

        assert updated_user.username == 'updated_Mirelle'
        assert updated_user.email == 'updated@pytest.com'
        assert updated_user.first_name == 'updated first name'
        assert updated_user.last_name == 'updated last name'
        assert updated_user.role_of.role == 'Technical support'

        assert data['password'] == 'test012345678'

    def test_delete_user(self, api_client_manager):

        user_to_delete = User.objects.create_user(username='Mirelle',
                                                  email='pouet@pouet.com',
                                                  password='test01234')
        user_role_to_delete = UserRole.objects.create(user=user_to_delete, role='Manager')

        # --
        response = api_client_manager.delete(f"/users/{user_to_delete.pk}/")

        assert response.status_code == 204
        assert User.objects.filter(pk=user_to_delete.pk).count() == 0
        assert User.objects.filter(pk=user_role_to_delete.pk).count() == 0
