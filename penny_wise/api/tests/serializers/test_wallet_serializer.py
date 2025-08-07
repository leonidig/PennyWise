import pytest
from api.models import User, Currency, Wallet
from api.serializers.wallet_serializer import WalletSerializer

@pytest.mark.django_db
def test_wallet_serializer_valid():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    currency = Currency.objects.create(code="USD", symbol="$")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=100)
    serializer = WalletSerializer(wallet)
    data = serializer.data
    assert data["balance"] == "100.00"
    assert data["currency"] == currency.id
    assert data["user"] == user.id

@pytest.mark.django_db
def test_wallet_serializer_create():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    currency = Currency.objects.create(code="USD", symbol="$")
    data = {"currency": currency.id, "balance": 200}
    serializer = WalletSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(user=user)
    assert instance.balance == 200
    assert instance.currency == currency
    assert instance.user == user

@pytest.mark.django_db
def test_wallet_serializer_missing_currency():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    data = {"balance": 100}
    serializer = WalletSerializer(data=data)
    assert not serializer.is_valid()
    assert "currency" in serializer.errors

@pytest.mark.django_db
def test_wallet_serializer_invalid_balance():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    currency = Currency.objects.create(code="USD", symbol="$")
    data = {"currency": currency.id, "balance": "not_a_number"}
    serializer = WalletSerializer(data=data)
    assert not serializer.is_valid()
    assert "balance" in serializer.errors 