from django.utils import timezone
from domain.entities.user import User
from domain.entities.wallet import Wallet


class CreateUserUseCase:
    def __init__(self, user_repository, wallet_repository):
        self.user_repository = user_repository
        self.wallet_repository = wallet_repository

    def execute(self, name: str, cpf: str, password: str) -> User:
        user = User(
            id=None, name=name, cpf=cpf, password=password, created_at=timezone.now()
        )

        user = self.user_repository.save(user)

        wallet = Wallet(
            id=None,
            cpf=cpf,
            balance=0.0,  # Inicializa com saldo zero
            created_at=timezone.now(),
        )

        self.wallet_repository.save(wallet)

        return user
