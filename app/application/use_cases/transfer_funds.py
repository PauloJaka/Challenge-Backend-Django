from domain.entities.wallet import Wallet
from domain.exceptions.insufficient_balance import InsufficientBalanceError


class TransferFundsUseCase:
    def __init__(self, wallet_repository, notification_service):
        self.wallet_repository = wallet_repository
        self.notification_service = notification_service

    def execute(self, amount: float, source_cpf: str, target_cpf: str):
        source_wallet = self.wallet_repository.get_wallet(source_cpf)
        target_wallet = self.wallet_repository.get_wallet(target_cpf)

        if source_wallet.balance < amount:
            raise (InsufficientBalanceError)

        source_wallet.balance -= amount
        target_wallet.balance += amount

        self.wallet_repository.save(source_wallet)
        self.wallet_repository.save(target_wallet)

        self.notification_service.send_notification(
            f"Transferência de R${amount} realizada com sucesso."
        )
