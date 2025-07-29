from rest_framework import viewsets
from ..models import Transaction
from ..serializers.transaction_serializer import TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)

    def perform_create(self, serializer):
        transaction = serializer.save()
        self.update_wallet_balance(transaction.wallet)

    def perform_update(self, serializer):
        transaction = serializer.save()
        self.update_wallet_balance(transaction.wallet)

    def perform_destroy(self, instance):
        wallet = instance.wallet
        instance.delete()
        self.update_wallet_balance(wallet)

    def update_wallet_balance(self, wallet):
        income = wallet.transactions.filter(category__is_income=True).aggregate(total=Sum('amount'))['total'] or 0
        expense = wallet.transactions.filter(category__is_income=False).aggregate(total=Sum('amount'))['total'] or 0
        wallet.balance = income - expense
        wallet.save()
