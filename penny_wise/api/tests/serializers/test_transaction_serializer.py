import pytest
from api.models import User, Category, Currency, Wallet, Transaction
from api.serializers.transaction_serializer import TransactionSerializer

@pytest.mark.django_db
def test_transaction_serializer_valid():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    currency = Currency.objects.create(code="USD", symbol="$")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=100)
    category = Category.objects.create(name="Food", is_income=False, user=user)
    transaction = Transaction.objects.create(category=category, wallet=wallet, amount=50, comment="Test")
    serializer = TransactionSerializer(transaction)
    data = serializer.data
    assert data["amount"] == 50
    assert data["category"] == category.id
    assert data["wallet"] == wallet.id
    assert data["comment"] == "Test"

@pytest.mark.django_db
def test_transaction_serializer_create():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    currency = Currency.objects.create(code="USD", symbol="$")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=100)
    category = Category.objects.create(name="Food", is_income=False, user=user)
    data = {"category": category.id, "wallet": wallet.id, "amount": 30, "comment": "Test2"}
    serializer = TransactionSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.amount == 30
    assert instance.category == category
    assert instance.wallet == wallet
    assert instance.comment == "Test2"

@pytest.mark.django_db
def test_transaction_serializer_missing_category():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    currency = Currency.objects.create(code="USD", symbol="$")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=100)
    data = {"wallet": wallet.id, "amount": 10}
    serializer = TransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert "category" in serializer.errors

@pytest.mark.django_db
def test_transaction_serializer_invalid_amount():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    currency = Currency.objects.create(code="USD", symbol="$")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=100)
    category = Category.objects.create(name="Food", is_income=False, user=user)
    data = {"category": category.id, "wallet": wallet.id, "amount": "not_an_int"}
    serializer = TransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert "amount" in serializer.errors

@pytest.mark.django_db
def test_transaction_serializer_invalid_wallet():
    user = User.objects.create_user(email="user@example.com", password="testpass")
    category = Category.objects.create(name="Food", is_income=False, user=user)
    data = {"category": category.id, "wallet": 9999, "amount": 10}
    serializer = TransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert "wallet" in serializer.errors 