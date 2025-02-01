from unittest.mock import Mock
from application.use_cases.create_user import CreateUserUseCase
from domain.entities.user import User
from domain.entities.wallet import Wallet
from django.utils import timezone
import pytest


def test_create_user_creates_wallet():
    user_repo_mock = Mock()
    wallet_repo_mock = Mock()

    use_case = CreateUserUseCase(user_repo_mock, wallet_repo_mock)

    name = "Alice"
    cpf = "12345678909"
    password = "senha123"

    returned_user = use_case.execute(name, cpf, password)

    user_repo_mock.save.assert_called_once()
    saved_user = user_repo_mock.save.call_args[0][0]

    assert saved_user.name == name
    assert saved_user.cpf == cpf
    assert saved_user.password == password
    assert saved_user.id is None

    wallet_repo_mock.save.assert_called_once()
    saved_wallet = wallet_repo_mock.save.call_args[0][0]

    assert saved_wallet.cpf == cpf
    assert saved_wallet.balance == 0.0
    assert isinstance(saved_wallet, Wallet)
