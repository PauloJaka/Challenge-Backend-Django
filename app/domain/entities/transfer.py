from django.utils import timezone


class Transfer:
    def __init__(
        self,
        id: int,
        source_cpf: str,
        target_cpf: str,
        amount: float,
        date: timezone,
    ):
        self.id = id
        self.source_cpf = source_cpf
        self.target_cpf = target_cpf
        self.amount = amount
        self.date = date
