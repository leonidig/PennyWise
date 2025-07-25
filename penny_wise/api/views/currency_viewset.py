from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..models import Currency
from ..serializers.currency_serializer import CurrencySerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAdminUser]
    swagger_schema_fields = {"tags": ["Currency"]}
