import pytest
from django.utils import timezone
from domain.entities.user import User
from domain.entities.wallet import Wallet


def test_user_creation():
    user = User(id=1, name="Alice", cpf="12345678909", password="senha_secreta")
    assert user.created_at.tzinfo == timezone.get_current_timezone()


def test_wallet_transaction():
    wallet = Wallet(id=1, cpf="12345678909", balance=100)
    wallet.add_balance(50)
    assert wallet.last_transaction_date.tzinfo == timezone.get_current_timezone()
