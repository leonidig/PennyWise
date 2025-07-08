from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema_view, extend_schema
from ..models import Currency
from ..serializers.currency_serializer import CurrencySerializer


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

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
