import pytest
from api.models import Currency
from api.serializers.currency_serializer import CurrencySerializer

@pytest.mark.django_db
def test_currency_serializer_valid():
    currency = Currency.objects.create(code="USD", symbol="$")
    serializer = CurrencySerializer(currency)
    data = serializer.data
    assert data["code"] == "USD"
    assert data["symbol"] == "$"

@pytest.mark.django_db
def test_currency_serializer_create():
    data = {"code": "EUR", "symbol": "€"}
    serializer = CurrencySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.code == "EUR"
    assert instance.symbol == "€"

@pytest.mark.django_db
def test_currency_serializer_missing_code():
    data = {"symbol": "$"}
    serializer = CurrencySerializer(data=data)
    assert not serializer.is_valid()
    assert "code" in serializer.errors

@pytest.mark.django_db
def test_currency_serializer_long_code():
    data = {"code": "TOOLONGCODE", "symbol": "$"}
    serializer = CurrencySerializer(data=data)
    assert not serializer.is_valid()
    assert "code" in serializer.errors

@pytest.mark.django_db
def test_currency_serializer_empty_symbol():
    data = {"code": "USD", "symbol": ""}
    serializer = CurrencySerializer(data=data)
    assert not serializer.is_valid()
    assert "symbol" in serializer.errors 