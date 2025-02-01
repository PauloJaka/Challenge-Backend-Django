import pytest
from django.utils import timezone
from domain.entities.user import User
from domain.entities.wallet import Wallet


@pytest.mark.django_db
def test_user_creation():
    user = User(id=1, name="Alice", cpf="12345678909", password="senha_secreta")

    user_created_at = user.created_at.astimezone(timezone.get_current_timezone())

    assert user_created_at.tzinfo == timezone.get_current_timezone()


@pytest.mark.django_db
def test_wallet_transaction():
    wallet = Wallet(id=1, cpf="12345678909", balance=100)
    wallet.add_balance(50)

    wallet_last_transaction_date = wallet.last_transaction_date.astimezone(
        timezone.get_current_timezone()
    )

    assert wallet_last_transaction_date.tzinfo == timezone.get_current_timezone()
