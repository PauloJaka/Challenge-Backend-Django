import pytest
from unittest.mock import Mock
from django.utils import timezone
from domain.entities.user import User
from application.use_cases.authentication_use_case import AuthenticationUseCase


class TestAuthenticationUseCase:
    def setup_method(self):
        self.jwt_secret = "test_secret"
        self.repo_mock = Mock()
        self.use_case = AuthenticationUseCase(self.repo_mock, self.jwt_secret)

        # Cria uma senha com hash para os testes
        self.plain_password = "senha123"
        self.hashed_password = AuthenticationUseCase.hash_password(self.plain_password)

        self.test_user = User(
            id=1,
            name="Test User",
            cpf="12345678900",
            password=self.hashed_password,
            created_at=timezone.now(),
        )

    def test_successful_authentication(self):
        
        self.repo_mock.find_by_cpf.return_value = self.test_user

        # Act
        result = self.use_case.execute(
            cpf=self.test_user.cpf, password=self.plain_password
        )

        # Assert
        assert result.authenticated == True
        assert result.token is not None
        assert result.error is None

    def test_authentication_with_invalid_password(self):
        
        self.repo_mock.find_by_cpf.return_value = self.test_user

        # Act
        result = self.use_case.execute(
            cpf=self.test_user.cpf, password="wrong_password"
        )

        # Assert
        assert result.authenticated == False
        assert result.error == "Credenciais inválidas"
        assert result.token is None

    def test_authentication_with_nonexistent_user(self):
        
        self.repo_mock.find_by_cpf.return_value = None

        # Act
        result = self.use_case.execute(cpf="nonexistent", password="any_password")

        # Assert
        assert result.authenticated == False
        assert result.error == "Usuário não encontrado"
        assert result.token is None

    def test_generated_token_contains_user_data(self):
        
        self.repo_mock.find_by_cpf.return_value = self.test_user

        # Act
        result = self.use_case.execute(
            cpf=self.test_user.cpf, password=self.plain_password
        )

        import jwt

        payload = jwt.decode(result.token, self.jwt_secret, algorithms=["HS256"])

        # Assert
        assert payload["user_id"] == self.test_user.id
        assert payload["cpf"] == self.test_user.cpf
