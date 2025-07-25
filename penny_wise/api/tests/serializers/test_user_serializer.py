import pytest
from api.models import User
from api.serializers.user_serializer import UserSerializer

@pytest.mark.django_db
def test_user_serializer_valid():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    serializer = UserSerializer(user)
    data = serializer.data
    assert data["email"] == "user@example.com"
    assert "id" in data

@pytest.mark.django_db
def test_user_serializer_missing_email():
    data = {"password": "testpass"}
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "email" in serializer.errors

@pytest.mark.django_db
def test_user_serializer_invalid_email():
    data = {"email": "not-an-email", "password": "testpass"}
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "email" in serializer.errors 