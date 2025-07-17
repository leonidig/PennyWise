from rest_framework import viewsets
from ..models import Wallet
from ..serializers.wallet_serializer import WalletSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(tags=['Wallet']),
    retrieve=extend_schema(tags=['Wallet']),
    create=extend_schema(tags=['Wallet']),
    update=extend_schema(tags=['Wallet']),
    partial_update=extend_schema(tags=['Wallet']),
    destroy=extend_schema(tags=['Wallet']),
)


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)