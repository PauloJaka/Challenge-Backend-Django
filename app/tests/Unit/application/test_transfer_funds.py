from unittest.mock import Mock
import pytest
from application.use_cases.transfer_funds import TransferFundsUseCase
from domain.entities.wallet import Wallet
from domain.exceptions.insufficient_balance import InsufficientBalanceError

def test_transfer_funds():
    wallet_repo = Mock()
    notification_service = Mock()
    
    source_wallet = Wallet(id=1, cpf="12345678909", balance=200.0)
    target_wallet = Wallet(id=2, cpf="98765432100", balance=0.0)
    
    wallet_repo.get_wallet.side_effect = [source_wallet, target_wallet]
    
    use_case = TransferFundsUseCase(wallet_repo, notification_service)
    use_case.execute(amount=150.0, source_cpf="12345678909", target_cpf="98765432100")
    
    assert source_wallet.balance == 50.0
    assert target_wallet.balance == 150.0
    wallet_repo.save.assert_any_call(source_wallet)
    wallet_repo.save.assert_any_call(target_wallet)
    notification_service.send_notification.assert_called()

def test_transfer_funds_insufficient_balance():
    wallet_repo = Mock()
    notification_service = Mock()
    
    source_wallet = Wallet(id=1, cpf="12345678909", balance=100.0)
    target_wallet = Wallet(id=2, cpf="98765432100", balance=0.0)
    
    wallet_repo.get_wallet.side_effect = [source_wallet, target_wallet]
    
    use_case = TransferFundsUseCase(wallet_repo, notification_service)
    
    with pytest.raises(InsufficientBalanceError):
        use_case.execute(amount=150.0, source_cpf="12345678909", target_cpf="98765432100")