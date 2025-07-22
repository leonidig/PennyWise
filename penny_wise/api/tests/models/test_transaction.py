import pytest
from penny_wise.api.models import User, Category, Currency, Wallet, Transaction
from django.urls import reverse

@pytest.mark.django_db
def test_transaction_create():
    user = User.objects.create_user(email="user3@example.com", password="testpass")
    currency = Currency.objects.create(code="UAH", symbol="₴")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=500)
    category = Category.objects.create(name="Shopping", is_income=False, user=user)
    transaction = Transaction.objects.create(category=category, wallet=wallet, amount=250, comment="Test purchase")
    assert transaction.category == category
    assert transaction.wallet == wallet
    assert transaction.amount == 250
    assert transaction.comment == "Test purchase"
    assert str(transaction) == f"250 - {category.name}"

@pytest.mark.django_db
def test_transaction_create_missing_fields(api_client, super_user):
    api_client.force_authenticate(super_user)
    url = reverse("transaction-list")
    data = {"amount": 100}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 400
    assert "category" in response.data
    assert "wallet" in response.data

@pytest.mark.django_db
def test_transaction_create_invalid_amount(api_client, super_user):
    api_client.force_authenticate(super_user)
    currency = Currency.objects.create(code="UAH", symbol="₴")
    wallet = Wallet.objects.create(user=super_user, currency=currency, balance=500)
    category = Category.objects.create(name="Shopping", is_income=False, user=super_user)
    url = reverse("transaction-list")
    data = {"category": category.id, "wallet": wallet.id, "amount": "not_an_int"}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 400
    assert "amount" in response.data

@pytest.mark.django_db
def test_transaction_create_invalid_category(api_client, super_user):
    api_client.force_authenticate(super_user)
    currency = Currency.objects.create(code="UAH", symbol="₴")
    wallet = Wallet.objects.create(user=super_user, currency=currency, balance=500)
    url = reverse("transaction-list")
    data = {"category": 9999, "wallet": wallet.id, "amount": 100}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 400
    assert "category" in response.data

@pytest.mark.django_db
def test_transaction_update_amount():
    user = User.objects.create_user(email="user3@example.com", password="testpass")
    currency = Currency.objects.create(code="UAH", symbol="₴")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=500)
    category = Category.objects.create(name="Shopping", is_income=False, user=user)
    transaction = Transaction.objects.create(category=category, wallet=wallet, amount=250, comment="Test purchase")
    transaction.amount = 300
    transaction.save()
    assert Transaction.objects.get(id=transaction.id).amount == 300

@pytest.mark.django_db
def test_transaction_delete():
    user = User.objects.create_user(email="user3@example.com", password="testpass")
    currency = Currency.objects.create(code="UAH", symbol="₴")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=500)
    category = Category.objects.create(name="Shopping", is_income=False, user=user)
    transaction = Transaction.objects.create(category=category, wallet=wallet, amount=250, comment="Test purchase")
    transaction_id = transaction.id
    transaction.delete()
    assert not Transaction.objects.filter(id=transaction_id).exists()

@pytest.mark.django_db
def test_transaction_get_by_category():
    user = User.objects.create_user(email="user3@example.com", password="testpass")
    currency = Currency.objects.create(code="UAH", symbol="₴")
    wallet = Wallet.objects.create(user=user, currency=currency, balance=500)
    category = Category.objects.create(name="Shopping", is_income=False, user=user)
    transaction = Transaction.objects.create(category=category, wallet=wallet, amount=250, comment="Test purchase")
    found = Transaction.objects.get(category=category)
    assert found == transaction 