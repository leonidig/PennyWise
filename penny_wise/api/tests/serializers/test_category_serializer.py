import pytest
from ..models import Category, User
from ..serializers.category_serializer import CategorySerializer

@pytest.mark.django_db
def test_category_serializer_valid():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    category = Category.objects.create(name="Food", is_income=False, user=user)
    serializer = CategorySerializer(category)
    data = serializer.data
    assert data["name"] == "Food"
    assert data["is_income"] is False
    assert data["user"] == user.id

@pytest.mark.django_db
def test_category_serializer_create():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    data = {"name": "Transport", "is_income": True}
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(user=user)
    assert instance.name == "Transport"
    assert instance.is_income is True
    assert instance.user == user

@pytest.mark.django_db
def test_category_serializer_missing_name():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    data = {"is_income": False}
    serializer = CategorySerializer(data=data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors

@pytest.mark.django_db
def test_category_serializer_invalid_is_income():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    data = {"name": "Food", "is_income": "not_bool"}
    serializer = CategorySerializer(data=data)
    assert not serializer.is_valid()
    assert "is_income" in serializer.errors 