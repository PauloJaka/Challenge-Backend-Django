from django.utils import timezone


class User:
    def __init__(
        self,
        id: int,
        name: str,
        cpf: str,
        password: str,
        created_at: timezone.datetime = None,
    ):
        self.id = id
        self.name = name
        self.cpf = self._validate_cpf(cpf)
        self.password = password
        self.created_at = created_at if created_at else timezone.now()

    def _validate_cpf(self, cpf: str) -> str:
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF inválido")
        return cpf
