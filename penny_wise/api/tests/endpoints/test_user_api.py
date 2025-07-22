import pytest
from django.urls import reverse
from ..models import User

@pytest.mark.django_db
def test_register_api(api_client):
    url = reverse("register")
    data = {"email": "newuser@example.com", "password": "testpass123"}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 201
    assert "email" in response.data

@pytest.mark.django_db
def test_login_api_success(api_client, super_user):
    url = reverse("login")
    data = {"email": "admin@example.com", "password": "adminpass"}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 200
    assert "token" in response.data or "access" in response.data

@pytest.mark.django_db
def test_login_api_fail(api_client):
    url = reverse("login")
    data = {"email": "notfound@example.com", "password": "wrongpass"}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code in (400, 401)

@pytest.mark.django_db
def test_protected_api_unauthorized(api_client):
    url = reverse("category-list")
    response = api_client.get(url)
    assert response.status_code in (401, 403) 