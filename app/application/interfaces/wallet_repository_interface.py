from abc import ABC, abstractmethod
from domain.entities.wallet import Wallet


class WalletRepository(ABC):
    @abstractmethod
    def save(self, wallet: Wallet) -> Wallet:
        pass

    @abstractmethod
    def find_by_cpf(self, cpf: str) -> Wallet:
        pass

    @abstractmethod
    def update_balance(self, cpf: str, amount: float) -> Wallet:
        pass
