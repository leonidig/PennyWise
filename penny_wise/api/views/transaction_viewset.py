from rest_framework import viewsets
from ..models import Transaction
from ..serializers.transaction_serializer import TransactionSerializer
from rest_framework.permissions import IsAuthenticated


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    swagger_schema_fields = {"tags": ["Transaction"]}

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)