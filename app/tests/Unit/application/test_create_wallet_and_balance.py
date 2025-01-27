from unittest.mock import Mock
import pytest
from django.utils import timezone
from application.use_cases.create_wallet import CreateWalletUseCase


def test_create_wallet_with_zero_balance():
    # Arrange
    repo_mock = Mock()
    use_case = CreateWalletUseCase(repo_mock)
    test_cpf = "12345678900"

    before_execution = timezone.now()

    returned_wallet = use_case.execute(cpf=test_cpf)

    # Capture time after execution
    after_execution = timezone.now()

    # Get wallet that was passed to save
    saved_wallet = repo_mock.save.call_args[0][0]

    # Assert
    assert saved_wallet.cpf == test_cpf
    assert saved_wallet._balance == 0.0
    assert saved_wallet.id is None
    assert before_execution <= saved_wallet.created_at <= after_execution
    assert saved_wallet.last_transaction_date == saved_wallet.created_at

    repo_mock.save.assert_called_once()
    assert returned_wallet == repo_mock.save.return_value


def test_create_wallet_with_initial_balance():
    repo_mock = Mock()
    use_case = CreateWalletUseCase(repo_mock)
    test_cpf = "12345678900"
    initial_balance = 100.0

    returned_wallet = use_case.execute(cpf=test_cpf, initial_balance=initial_balance)

    saved_wallet = repo_mock.save.call_args[0][0]

    assert saved_wallet._balance == initial_balance
    repo_mock.save.assert_called_once()


def test_create_wallet_with_negative_balance_raises_error():
    repo_mock = Mock()
    use_case = CreateWalletUseCase(repo_mock)
    test_cpf = "12345678900"
    negative_balance = -100.0

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(cpf=test_cpf, initial_balance=negative_balance)

    assert str(exc_info.value) == "Saldo inicial não pode ser negativo"
    repo_mock.save.assert_not_called()
