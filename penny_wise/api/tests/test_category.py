import pytest
from django.urls import reverse
from ..models import Category



@pytest.mark.django_db
def test_create_category(api_client, super_user):
    api_client.force_authenticate(super_user)

    url = reverse("category-list")
    data = {
        "name": "Food",
        "is_income": False
    }
    response = api_client.post(url, data=data)

    assert response.status_code == 201
    assert response.data.get("name") == "Food"
    assert Category.objects.filter(name="Food", user=super_user).exists()


