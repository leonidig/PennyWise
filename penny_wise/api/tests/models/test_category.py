import pytest
from django.urls import reverse
from penny_wise.api.models import Category


@pytest.mark.django_db
def test_create_category(api_client, super_user):
    api_client.force_authenticate(super_user)

    url = reverse("category-list")
    data = {
        "name": "Food",
        "is_income": False
    }
    response = api_client.post(url, data=data, format="json")

    if response.status_code != 201:
        print("CREATE ERROR:", response.data)
    assert response.status_code == 201
    assert response.data.get("name") == "Food"
    assert Category.objects.filter(name="Food", user=super_user).exists()


@pytest.mark.django_db
def test_category_list(api_client, super_user):
    api_client.force_authenticate(super_user)
    url = reverse("category-list")
    Category.objects.create(name="Food", is_income=False, user=super_user)
    Category.objects.create(name="Salary", is_income=True, user=super_user)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    names = [cat["name"] for cat in response.data]
    assert "Food" in names and "Salary" in names


@pytest.mark.django_db
def test_category_detail_fields(api_client, super_user):
    api_client.force_authenticate(super_user)
    category = Category.objects.create(name="Food", is_income=False, user=super_user)
    url = reverse("category-detail", args=[category.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == "Food"


@pytest.mark.django_db
def test_category_update_name(api_client, super_user):
    api_client.force_authenticate(super_user)
    category = Category.objects.create(name="Food", is_income=False, user=super_user)
    url = reverse("category-detail", args=[category.id])
    data = {"name": "Groceries", "is_income": False}
    response = api_client.put(url, data=data, format="json")
    assert response.status_code == 200
    category.refresh_from_db()
    assert category.name == "Groceries"


@pytest.mark.django_db
def test_category_delete(api_client, super_user):
    api_client.force_authenticate(super_user)
    category = Category.objects.create(name="Food", is_income=False, user=super_user)
    url = reverse("category-detail", args=[category.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Category.objects.filter(id=category.id).exists()


