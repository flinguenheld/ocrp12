import pytest

from rest_framework.test import APIClient
import logging

from epic_crm.users.models import User


# Logging --
logger = logging.getLogger('django')


@pytest.fixture(scope="session", autouse=True)
def prout():
    logger.info('========================= PYTEST SESSION START =========================')
    yield
    logger.info('========================= PYTEST SESSION  END  =========================')


# --
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def api_client_manager():
    client = APIClient()
    return add_user_then_connect(client,
                                 email='manager@pytest.com',
                                 password='test01234',
                                 role='Manager')


@pytest.fixture
def api_client_salesperson():
    client = APIClient()
    return add_user_then_connect(client,
                                 email='salesperson@pytest.com',
                                 password='test01234',
                                 role='Salesperson')


@pytest.fixture
def api_client_technical_support():
    client = APIClient()
    return add_user_then_connect(client,
                                 email='technical_support@pytest.com',
                                 password='test01234',
                                 role='Technical support')


def add_user_then_connect(client, email, password, role):

    User.objects.create_user(email=email, password=password, role=role)

    response = client.post("/login/", data={"email": email, "password": password})
    data = response.json()

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {data['access']}")
    return client


