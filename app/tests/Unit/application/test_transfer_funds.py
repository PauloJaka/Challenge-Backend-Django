from unittest.mock import Mock
import pytest
from application.use_cases.transfer_funds import TransferFundsUseCase
from domain.entities.wallet import Wallet
from domain.exceptions.insufficient_balance import InsufficientBalanceError
from decimal import Decimal


def test_transfer_funds():
    # Criando mocks para as dependências
    wallet_repo = Mock()
    transfer_repo = Mock()
    notification_service = Mock()

    # Definindo as carteiras de origem e destino
    source_wallet = Wallet(id=1, cpf="12345678909", balance=Decimal("200.00"))
    target_wallet = Wallet(id=2, cpf="98765432100", balance=Decimal("0.00"))

    # Configurando os mocks
    wallet_repo.get_wallet.side_effect = [source_wallet, target_wallet]

    # Instanciando o use case com todos os parâmetros necessários
    use_case = TransferFundsUseCase(
        wallet_repository=wallet_repo,
        transfer_repository=transfer_repo,  # Passando o repositório de transferências
        notification_service=notification_service,
    )

    # Executando a transferência
    use_case.execute(
        amount=Decimal("150.00"), source_cpf="12345678909", target_cpf="98765432100"
    )

    # Verificando os saldos após a transferência
    assert source_wallet.balance == Decimal("50.00")
    assert target_wallet.balance == Decimal("150.00")

    # Verificando se os métodos de salvar as carteiras e notificar foram chamados
    wallet_repo.save.assert_any_call(source_wallet)
    wallet_repo.save.assert_any_call(target_wallet)
    notification_service.send_transfer_notification.assert_called()


def test_transfer_funds_insufficient_balance():
    wallet_repo = Mock()
    transfer_repo = Mock()
    notification_service = Mock()

    # Carteira de origem com saldo insuficiente
    source_wallet = Wallet(id=1, cpf="12345678909", balance=Decimal("100.00"))
    target_wallet = Wallet(id=2, cpf="98765432100", balance=Decimal("0.00"))

    wallet_repo.get_wallet.side_effect = [source_wallet, target_wallet]

    use_case = TransferFundsUseCase(
        wallet_repository=wallet_repo,
        transfer_repository=transfer_repo,
        notification_service=notification_service,
    )

    # Verificando se o erro de saldo insuficiente é lançado
    with pytest.raises(ValueError) as exc_info:
        use_case.execute(
            amount=Decimal("150.00"), source_cpf="12345678909", target_cpf="98765432100"
        )

    # Validando a mensagem do erro
    assert str(exc_info.value) == "Saldo insuficiente na carteira de origem."
