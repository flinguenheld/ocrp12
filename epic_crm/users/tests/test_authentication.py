import pytest

from django.contrib.auth.models import User


@pytest.mark.django_db
class TestAuthentication:

    def test_login_fail(self, client):

        response = client.post("/login/",
                               data={"username": "jean", "password": "nopassword"})
        data = response.json()

        assert response.status_code == 401
        assert "No active account found" in data['detail']

    def test_login_then_refresh_success(self, client):

        user = User.objects.create_user(username='jean', email='manager@pytest.com', password='test01234')
        user.role_of.role = 'Manager'

        # --
        response_login = client.post("/login/",
                                     data={"username": "jean", "password": "test01234"})
        data = response_login.json()

        assert response_login.status_code == 200
        assert "access" in data
        assert "refresh" in data

        response_refresh = client.post("/refresh/",
                                       data={"refresh": data['refresh']})
        assert response_refresh.status_code == 200
        assert "access" in data
