import requests


class TestUserManagement:

    ENDPOINT = "http://localhost:8000/"

    def test_create_user(self):

        response_list = requests.post(self.ENDPOINT + "user/", json={"email": "test@test.com", "password": "01234"})
        data = response_login.json()

        assert response_login.status_code == 200
        assert "access" in data
        assert "refresh" in data
