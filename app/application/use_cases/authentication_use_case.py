from dataclasses import dataclass
import jwt
from datetime import datetime, timedelta
import bcrypt
from domain.entities.user import User
from application.interfaces.user_repository_interface import UserRepository


@dataclass
class AuthenticationResult:
    authenticated: bool
    token: str = None
    error: str = None


class AuthenticationUseCase:
    def __init__(self, user_repository: UserRepository, jwt_secret: str):
        self.user_repository = user_repository
        self.jwt_secret = jwt_secret

    def execute(self, cpf: str, password: str) -> AuthenticationResult:
        user = self.user_repository.find_by_cpf(cpf)

        if not user:
            return AuthenticationResult(
                authenticated=False, error="Usuário não encontrado"
            )

        # Verifica a senha com bcrypt
        if not self._verify_password(password, user.password):
            return AuthenticationResult(
                authenticated=False, error="Credenciais inválidas"
            )

        # Gera o token JWT
        token = self._generate_token(user)

        return AuthenticationResult(authenticated=True, token=token)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def _generate_token(self, user: User) -> str:
        payload = {
            "user_id": user.id,
            "cpf": user.cpf,
            "exp": datetime.utcnow() + timedelta(days=1),
        }

        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
