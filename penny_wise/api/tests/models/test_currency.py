import pytest
from api.models import Currency
from django.urls import reverse

@pytest.mark.django_db
def test_currency_create():
    currency = Currency.objects.create(code="USD", symbol="$")
    assert currency.code == "USD"
    assert currency.symbol == "$"
    assert str(currency) == "USD ($)"

@pytest.mark.django_db
def test_currency_create_missing_code(api_client, super_user):
    api_client.force_authenticate(super_user)
    url = reverse("currency-list")
    data = {"symbol": "$"}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 400
    assert "code" in response.data

@pytest.mark.django_db
def test_currency_create_long_code(api_client, super_user):
    api_client.force_authenticate(super_user)
    url = reverse("currency-list")
    data = {"code": "TOOLONGCODE", "symbol": "$"}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 400
    assert "code" in response.data

@pytest.mark.django_db
def test_currency_create_invalid_symbol(api_client, super_user):
    api_client.force_authenticate(super_user)
    url = reverse("currency-list")
    data = {"code": "USD", "symbol": ""}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == 400
    assert "symbol" in response.data

@pytest.mark.django_db
def test_currency_update():
    currency = Currency.objects.create(code="USD", symbol="$")
    currency.symbol = "$"
    currency.save()
    assert Currency.objects.get(id=currency.id).symbol == "$"

@pytest.mark.django_db
def test_currency_delete():
    currency = Currency.objects.create(code="USD", symbol="$")
    currency_id = currency.id
    currency.delete()
    assert not Currency.objects.filter(id=currency_id).exists()

@pytest.mark.django_db
def test_currency_get():
    Currency.objects.create(code="EUR", symbol="€")
    found = Currency.objects.get(code="EUR")
    assert found.symbol == "€" 