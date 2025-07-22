import pytest
from rest_framework.test import APIClient
from ..models import User

@pytest.fixture
def super_user(db):
    return User.objects.create_superuser(email="admin@example.com", password="adminpass")

@pytest.fixture
def api_client():
    return APIClient() 