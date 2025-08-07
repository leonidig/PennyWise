import pytest
from rest_framework.test import APIClient
from ..models import User

@pytest.fixture
def super_user(db):
    return User.objects.create_superuser(email="admin@example.com", password="adminpass")

@pytest.fixture
def api_client():
    return APIClient()
12333',
    )
    return user


@pytest.fixture
def api_client():
    return APIClient()