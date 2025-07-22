import pytest
from ..models import User, Currency, Wallet
from django.urls import reverse

@pytest.mark.django_db
def test_wallet_create():
    user = User.objects.create_user(email="user2@example.com", password="testpass")
    currency = Currency.objects.create(code="EUR", symbol="€")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=1000.50)
    assert wallet.user == user
    assert wallet.currency == currency
    assert wallet.balance == 1000.50
    assert str(wallet) == f"Wallet {user.email} [{currency}]"

@pytest.mark.django_db
def test_wallet_create_invalid_balance(api_client, super_user):
    api_client.force_authenticate(super_user)
    currency = Currency.objects.create(code="USD", symbol="$")
    url = reverse("wallet-list")
    data = {"user": super_user.id, "currency": currency.id, "balance": "not_a_float"}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 400
    assert "balance" in response.data

@pytest.mark.django_db
def test_wallet_create_missing_fields(api_client, super_user):
    api_client.force_authenticate(super_user)
    url = reverse("wallet-list")
    data = {"balance": 100}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 400
    assert "currency" in response.data

@pytest.mark.django_db
def test_wallet_create_invalid_currency(api_client, super_user):
    api_client.force_authenticate(super_user)
    url = reverse("wallet-list")
    data = {"currency": 9999, "balance": 100}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 400
    assert "currency" in response.data

@pytest.mark.django_db
def test_wallet_update_invalid_balance(api_client, super_user):
    api_client.force_authenticate(super_user)
    currency = Currency.objects.create(code="USD", symbol="$")
    wallet = Wallet.objects.create(user=super_user, currency=currency, balance=100)
    url = reverse("wallet-detail", args=[wallet.id])
    data = {"currency": currency.id, "balance": "not_a_float"}
    response = api_client.put(url, data=data, format="json")
    assert response.status_code == 400
    assert "balance" in response.data

@pytest.mark.django_db
def test_wallet_update_balance():
    user = User.objects.create_user(email="user1@example.com", password="user1password")
    currency = Currency.objects.create(code="EUR", symbol="€")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=100)
    wallet.balance = 200
    wallet.save()
    assert Wallet.objects.get(id=wallet.id).balance == 200

@pytest.mark.django_db
def test_wallet_delete():
    user = User.objects.create_user(email="user1@example.com", password="user1password")
    currency = Currency.objects.create(code="EUR", symbol="€")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=100)
    wallet_id = wallet.id
    wallet.delete()
    assert not Wallet.objects.filter(id=wallet_id).exists()

@pytest.mark.django_db
def test_wallet_get_by_user():
    user = User.objects.create_user(email="user1@example.com", password="user1password")
    currency = Currency.objects.create(code="EUR", symbol="€")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=100)
    found = Wallet.objects.get(user=user)
    assert found == wallet