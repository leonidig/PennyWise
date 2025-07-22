import pytest
from penny_wise.api.models import User

@pytest.mark.django_db
def test_user_create():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    assert user.email == "user@example.com"
    assert user.check_password("testpass")
    assert not user.is_staff
    assert not user.is_superuser

@pytest.mark.django_db
def test_superuser_create():
    superuser = User.objects.create_superuser(email="admin@example.com", password="adminpass")
    assert superuser.email == "admin@example.com"
    assert superuser.check_password("adminpass")
    assert superuser.is_staff
    assert superuser.is_superuser 

@pytest.mark.django_db
def test_user_update_email():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    user.email = "new@example.com"
    user.save()
    assert User.objects.get(id=user.id).email == "new@example.com"

@pytest.mark.django_db
def test_user_is_active_flag():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    user.is_active = False
    user.save()
    assert not User.objects.get(id=user.id).is_active

@pytest.mark.django_db
def test_user_delete():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    user_id = user.id
    user.delete()
    assert not User.objects.filter(id=user_id).exists() 