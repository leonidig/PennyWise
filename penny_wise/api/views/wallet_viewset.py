from rest_framework import viewsets
from ..models import Wallet
from ..serializers.wallet_serializer import WalletSerializer
from rest_framework.permissions import IsAuthenticated


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    swagger_schema_fields = {"tags": ["Wallet"]}
 
    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)