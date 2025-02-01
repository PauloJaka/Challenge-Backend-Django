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

    # Act
    returned_wallet = use_case.execute(cpf=test_cpf)

    # Capture time after execution
    after_execution = timezone.now()

    # Get wallet that was passed to save
    saved_wallet = repo_mock.save.call_args[0][0]

    # Assert
    assert saved_wallet.cpf == test_cpf, "CPF não foi passado corretamente"
    assert saved_wallet._balance == 0.0, "Saldo inicial deve ser zero"
    assert saved_wallet.id is None, "ID deve ser None antes de salvar"
    assert (
        before_execution <= saved_wallet.created_at <= after_execution
    ), "Data de criação fora do intervalo esperado"
    assert (
        saved_wallet.last_transaction_date == saved_wallet.created_at
    ), "Data da última transação deve ser igual à data de criação"

    repo_mock.save.assert_called_once(), "Repositório deve ser chamado uma vez"
    assert (
        returned_wallet == repo_mock.save.return_value
    ), "Carteira retornada deve ser a mesma que foi salva"


def test_create_wallet_with_initial_balance():
    # Arrange
    repo_mock = Mock()
    use_case = CreateWalletUseCase(repo_mock)
    test_cpf = "12345678900"
    initial_balance = 100.0

    # Act
    returned_wallet = use_case.execute(cpf=test_cpf, initial_balance=initial_balance)

    # Get wallet that was passed to save
    saved_wallet = repo_mock.save.call_args[0][0]

    # Assert
    assert saved_wallet.cpf == test_cpf, "CPF não foi passado corretamente"
    assert saved_wallet._balance == initial_balance, "Saldo inicial deve ser 100.0"
    repo_mock.save.assert_called_once(), "Repositório deve ser chamado uma vez"
    assert (
        returned_wallet == repo_mock.save.return_value
    ), "Carteira retornada deve ser a mesma que foi salva"


def test_create_wallet_with_negative_balance_raises_error():
    # Arrange
    repo_mock = Mock()
    use_case = CreateWalletUseCase(repo_mock)
    test_cpf = "12345678900"
    negative_balance = -100.0

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(cpf=test_cpf, initial_balance=negative_balance)

    # Assert
    assert (
        str(exc_info.value) == "Saldo inicial não pode ser negativo"
    ), "Mensagem de erro incorreta"
    repo_mock.save.assert_not_called(), "Repositório não deve ser chamado para saldo negativo"
