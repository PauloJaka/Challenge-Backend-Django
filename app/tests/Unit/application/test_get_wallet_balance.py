from unittest.mock import Mock
from application.use_cases.get_wallet_balance import GetWalletBalanceUseCase
from domain.entities.wallet import Wallet


def test_get_wallet_balance():
    # Mock do repositório
    wallet_repo = Mock()
    wallet = Wallet(id=1, cpf="12345678909", balance=100.0)
    wallet_repo.get_wallet.return_value = wallet

    # Caso de uso
    use_case = GetWalletBalanceUseCase(wallet_repo)
    result = use_case.execute("12345678909")

    # Verificações
    assert result == 100.0
    wallet_repo.get_wallet.assert_called_once_with("12345678909")


def test_get_wallet_balance_user_not_found():
    wallet_repo = Mock()
    wallet_repo.get_wallet.side_effect = Exception("Carteira não encontrada")

    use_case = GetWalletBalanceUseCase(wallet_repo)

    try:
        use_case.execute("00000000000")
    except Exception as e:
        assert str(e) == "Carteira não encontrada"
