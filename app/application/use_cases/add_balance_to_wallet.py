from domain.entities.wallet import Wallet
from domain.exceptions.wallet_not_found_execption import WalletNotFoundException
from infrastructure.repositories.django_wallet_repository import DjangoWalletRepository


class AddBalanceToWalletUseCase:
    def __init__(self, wallet_repository: DjangoWalletRepository):
        self.wallet_repository = wallet_repository

    def execute(self, cpf: str, amount: float) -> Wallet:
        if amount <= 0:
            raise ValueError("A quantidade a ser adicionada deve ser positiva")

        # Buscar a carteira
        wallet = self.wallet_repository.get_wallet(cpf)
        if not wallet:
            raise WalletNotFoundException("Carteira não encontrada")

        wallet.add_balance(amount)
        return self.wallet_repository.save(wallet)
