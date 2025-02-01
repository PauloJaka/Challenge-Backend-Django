"""
URL configuration for wallet_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from webapps.views import (
    ListTransfersView,
    CreateUserView,
    AddBalanceToWalletView,
    TransferFundsView,
    WalletBalanceView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # URL para criar usuario (POST)
    path("api/users/", CreateUserView.as_view(), name="create_user"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # URL para listagem de transferências (GET)
    path("wallet/transfers/", ListTransfersView.as_view(), name="list_transfers"),
    # URL para adicionar saldo na carteira (POST)
    path(
        "wallet/<str:cpf>/add_balance/",
        AddBalanceToWalletView.as_view(),
        name="add_balance_to_wallet",
    ),
    # URL para transferir fundos (POST)
    path("wallet/transfer/", TransferFundsView.as_view(), name="transfer_funds"),
    # URL para ver saldo (GET)
    path("api/wallet/balance/", WalletBalanceView.as_view(), name="wallet_balance"),
]
