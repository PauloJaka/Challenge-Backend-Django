from django.utils import timezone
from domain.entities.user import User

class CreateUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, name: str, cpf: str, password: str) -> User:
        user = User(
            id=None,
            name=name,
            cpf=cpf,
            password=password,
            created_at=timezone.now()  
        )
        return self.user_repository.save(user)