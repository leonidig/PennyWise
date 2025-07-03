from rest_framework import viewsets
from ..models import Transaction
from ..serializers.transaction_serializer import TransactionSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(tags=['Transaction']),
    retrieve=extend_schema(tags=['Transaction']),
    create=extend_schema(tags=['Transaction']),
    update=extend_schema(tags=['Transaction']),
    partial_update=extend_schema(tags=['Transaction']),
    destroy=extend_schema(tags=['Transaction']),
)
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer