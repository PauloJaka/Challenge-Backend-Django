from domain.entities.wallet import Wallet
from domain.exceptions.insufficient_balance import InsufficientBalanceError
from infrastructure.repositories.django_wallet_repository import DjangoWalletRepository
from typing import Any
from infrastructure.repositories.django_wallet_repository import DjangoWalletRepository
from decimal import Decimal
from infrastructure.repositories.django_transfer_repository import (
    DjangoTransferRepository,
)
from django.utils import timezone


class TransferFundsUseCase:
    def __init__(
        self,
        wallet_repository: DjangoWalletRepository,
        transfer_repository: DjangoTransferRepository,
        notification_service: Any,
    ):
        self.wallet_repository = wallet_repository
        self.transfer_repository = transfer_repository
        self.notification_service = notification_service

    def execute(self, amount: float, source_cpf: str, target_cpf: str) -> None:
        # Convertendo o valor para Decimal
        amount = Decimal(str(amount))

        # Buscando as carteiras
        source_wallet = self.wallet_repository.get_wallet(source_cpf)
        if source_wallet.balance < amount:
            raise ValueError("Saldo insuficiente na carteira de origem.")

        target_wallet = self.wallet_repository.get_wallet(target_cpf)

        # Realizando a transferência
        source_wallet.balance -= amount
        target_wallet.balance += amount

        # Salvando as carteiras
        self.wallet_repository.save(source_wallet)
        self.wallet_repository.save(target_wallet)

        # Salvando a transferência
        transfer = self.transfer_repository.save_transfer(
            source_cpf=source_cpf,
            target_cpf=target_cpf,
            amount=amount,
            date=timezone.now(),
        )

        # Enviando a notificação
        if self.notification_service:
            self.notification_service.send_transfer_notification(
                source_cpf, target_cpf, amount
            )
