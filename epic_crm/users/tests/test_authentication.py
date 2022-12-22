import pytest

from epic_crm.users.models import User


@pytest.mark.django_db
class TestAuthentication:

    def test_login_fail(self, client):

        response = client.post("/login/",
                               data={"email": "wrong@wrong.com", "password": "nopassword"})
        data = response.json()

        assert response.status_code == 401
        assert "No active account found" in data['detail']

    def test_login_then_refresh_success(self, client):

        User.objects.create_user(email='manager@pytest.com', password='test01234', role='Manager')

        # --
        response_login = client.post("/login/",
                                     data={"email": "manager@pytest.com", "password": "test01234"})
        data = response_login.json()

        assert response_login.status_code == 200
        assert "access" in data
        assert "refresh" in data

        response_refresh = client.post("/refresh/",
                                       data={"refresh": data['refresh']})
        assert response_refresh.status_code == 200
        assert "access" in data
