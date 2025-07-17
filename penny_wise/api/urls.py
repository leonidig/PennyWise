from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.category_viewset import CategoryViewSet
from api.views.currency_viewset import CurrencyViewSet
from api.views.wallet_viewset import WalletViewSet
from api.views.transaction_viewset import TransactionViewSet
from api.views.user_viewset import LoginView, RegisterView
from api.views.csrf import Csrf

router = DefaultRouter()

router.register(r'category', CategoryViewSet)
router.register(r'currency', CurrencyViewSet)
router.register(r'wallet', WalletViewSet)
router.register(r'transaction', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('csrf/', Csrf.as_view(), name='csrf'),
]
