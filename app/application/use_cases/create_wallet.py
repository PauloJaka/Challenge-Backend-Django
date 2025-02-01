from django.utils import timezone
from domain.entities.wallet import Wallet


class CreateWalletUseCase:
    def __init__(self, wallet_repository):
        self.wallet_repository = wallet_repository

    def execute(self, cpf: str, initial_balance: float = 0.0) -> Wallet:
        if initial_balance < 0:
            raise ValueError("Saldo inicial não pode ser negativo")

        wallet = Wallet(
            id=None, cpf=cpf, balance=initial_balance, created_at=timezone.now()
        )

        return self.wallet_repository.save(wallet)
