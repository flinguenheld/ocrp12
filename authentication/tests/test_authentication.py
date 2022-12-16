import requests


class TestAuthentication:

    ENDPOINT = "http://localhost:8000/"

    def test_login_fail(self):

        response = requests.post(self.ENDPOINT + "login/", json={"email": "wrong@wrong.com", "password": "01234"})
        data = response.json()

        assert response.status_code == 401
        assert "No active account found" in data['detail']

    def test_login_then_refresh_success(self):

        response_login = requests.post(self.ENDPOINT + "login/", json={"email": "test@test.com", "password": "01234"})
        data = response_login.json()

        assert response_login.status_code == 200
        assert "access" in data
        assert "refresh" in data

        response_refresh = requests.post(self.ENDPOINT + "refresh/", json={"refresh": data['refresh']})
        assert response_refresh.status_code == 200
        assert "access" in data
