from unittest.mock import Mock
from application.use_cases.create_user import CreateUserUseCase
from domain.entities.user import User
from django.utils import timezone
import pytest
from datetime import datetime


def test_create_user():
    repo_mock = Mock()

    use_case = CreateUserUseCase(repo_mock)

    name = "Alice"
    cpf = "12345678909"
    password = "senha123"

    before_execution = timezone.now()

    returned_user = use_case.execute(name, cpf, password)

    after_execution = timezone.now()

    saved_user = repo_mock.save.call_args[0][0]

    assert saved_user.name == name
    assert saved_user.cpf == cpf
    assert saved_user.password == password
    assert saved_user.id is None

    assert before_execution <= saved_user.created_at <= after_execution

    repo_mock.save.assert_called_once()

    # Verifica se o usuário retornado é o mesmo que foi retornado pelo repositório
    assert returned_user == repo_mock.save.return_value
