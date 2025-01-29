from django.utils import timezone

class Wallet:
    def __init__(
        self,
        id: int,
        cpf: str,
        balance: float,
        created_at: timezone.datetime = None,
        last_transaction_date: timezone.datetime = None,
    ):
        self.id = id
        self.cpf = cpf
        self._balance = balance
        self.created_at = created_at if created_at else timezone.now()
        self.last_transaction_date = (
            last_transaction_date if last_transaction_date else self.created_at
        )

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Saldo não pode ser negativo")
        self._balance = value

    def add_balance(self, amount: float, transaction_date: timezone.datetime = None):
        self.balance = self._balance + amount
        self.last_transaction_date = (
            transaction_date if transaction_date else timezone.now()
        )