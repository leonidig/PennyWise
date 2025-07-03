from rest_framework import viewsets
from ..models import Currency
from ..serializers.currency_serializer import CurrencySerializer
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(tags=['Currency']),
    retrieve=extend_schema(tags=['Currency']),
    create=extend_schema(tags=['Currency']),
    update=extend_schema(tags=['Currency']),
    partial_update=extend_schema(tags=['Currency']),
    destroy=extend_schema(tags=['Currency']),
)
class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer