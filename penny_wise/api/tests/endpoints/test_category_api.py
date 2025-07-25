import pytest
from django.urls import reverse
from api.models import Category

@pytest.mark.django_db
def test_category_list_api(api_client, super_user):
    api_client.force_authenticate(super_user)
    Category.objects.create(name="Food", is_income=False, user=super_user)
    Category.objects.create(name="Salary", is_income=True, user=super_user)
    url = reverse("category-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_category_retrieve_api(api_client, super_user):
    api_client.force_authenticate(super_user)
    category = Category.objects.create(name="Food", is_income=False, user=super_user)
    url = reverse("category-detail", args=[category.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == "Food"

@pytest.mark.django_db
def test_category_create_api_success(api_client, super_user):
    api_client.force_authenticate(super_user)
    url = reverse("category-list")
    data = {"name": "Transport", "is_income": False}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "Transport"

@pytest.mark.django_db
def test_category_create_api_fail(api_client, super_user):
    api_client.force_authenticate(super_user)
    url = reverse("category-list")
    data = {"is_income": False}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 400
    assert "name" in response.data

@pytest.mark.django_db
def test_category_update_api_success(api_client, super_user):
    api_client.force_authenticate(super_user)
    category = Category.objects.create(name="Food", is_income=False, user=super_user)
    url = reverse("category-detail", args=[category.id])
    data = {"name": "Groceries", "is_income": False}
    response = api_client.put(url, data=data, format="json")
    assert response.status_code == 200
    assert response.data["name"] == "Groceries"

@pytest.mark.django_db
def test_category_update_api_fail(api_client, super_user):
    api_client.force_authenticate(super_user)
    category = Category.objects.create(name="Food", is_income=False, user=super_user)
    url = reverse("category-detail", args=[category.id])
    data = {"is_income": False}
    response = api_client.put(url, data=data, format="json")
    assert response.status_code == 400
    assert "name" in response.data

@pytest.mark.django_db
def test_category_delete_api(api_client, super_user):
    api_client.force_authenticate(super_user)
    category = Category.objects.create(name="Food", is_income=False, user=super_user)
    url = reverse("category-detail", args=[category.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Category.objects.filter(id=category.id).exists()

@pytest.mark.django_db
def test_category_api_unauthorized(api_client):
    url = reverse("category-list")
    response = api_client.get(url)
    assert response.status_code in (401, 403) 