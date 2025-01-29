from django.test import TestCase
from django.utils import timezone
from domain.entities.user import User
from infrastructure.repositories.django_user_repository import DjangoUserRepository
import pytest
from django.utils import timezone
from infrastructure.repositories.django_wallet_repository import DjangoWalletRepository
from domain.entities.wallet import Wallet as CoreWallet
from infrastructure.models.wallet_model import DjangoWallet
from django.contrib.auth import get_user_model

class TestDjangoUserRepository(TestCase):
    def setUp(self):
        self.repository = DjangoUserRepository()
    
    def test_save_user_with_timezone(self):
        # Arrange
        user = User(
            id=None,
            name="Bob",
            cpf="98765432100",
            password="senha123",
            created_at=None
        )
        
        # Act
        saved_user = self.repository.save(user)
        
        # Assert
        self.assertIsNotNone(saved_user.id)
        self.assertEqual(saved_user.name, "Bob")
        self.assertEqual(saved_user.cpf, "98765432100")
        self.assertIsNotNone(saved_user.created_at)

@pytest.mark.django_db
def test_get_wallet():
    # Cria um usuário e uma carteira no banco de dados
    CustomUser = get_user_model()
    user = CustomUser.objects.create(cpf="12345678909", name="Alice", password="senha123")
    django_wallet = DjangoWallet.objects.create(cpf=user, balance=100.0)

    # Testa o repositório
    repo = DjangoWalletRepository()
    core_wallet = repo.get_wallet("12345678909")

    assert core_wallet.id == django_wallet.id
    assert core_wallet.cpf == "12345678909"
    assert core_wallet.balance == 100.0
    assert core_wallet.created_at == timezone.localtime(django_wallet.created_at)
    assert core_wallet.last_transaction_date == timezone.localtime(django_wallet.last_transaction_date)

@pytest.mark.django_db
def test_save_wallet():
    # Cria um usuário no banco de dados
    CustomUser = get_user_model()
    user = CustomUser.objects.create(cpf="12345678909", name="Alice", password="senha123")

    # Cria uma entidade Wallet
    core_wallet = CoreWallet(
        id=None,
        cpf="12345678909",
        balance=200.0,
        created_at=timezone.now(),
        last_transaction_date=timezone.now()
    )

    # Testa o repositório
    repo = DjangoWalletRepository()
    saved_wallet = repo.save(core_wallet)

    # Verifica se a carteira foi salva corretamente
    django_wallet = DjangoWallet.objects.get(cpf=user)
    assert saved_wallet.id == django_wallet.id
    assert saved_wallet.cpf == "12345678909"
    assert saved_wallet.balance == 200.0
    assert saved_wallet.created_at == timezone.localtime(django_wallet.created_at)
    assert saved_wallet.last_transaction_date == timezone.localtime(django_wallet.last_transaction_date)

@pytest.mark.django_db
def test_save_wallet_update():
    # Cria um usuário e uma carteira no banco de dados
    CustomUser = get_user_model()
    user = CustomUser.objects.create(cpf="12345678909", name="Alice", password="senha123")
    django_wallet = DjangoWallet.objects.create(cpf=user, balance=100.0)

    # Cria uma entidade Wallet com novos dados
    core_wallet = CoreWallet(
        id=django_wallet.id,
        cpf="12345678909",
        balance=300.0,
        created_at=timezone.now(),
        last_transaction_date=timezone.now()
    )

    # Testa o repositório
    repo = DjangoWalletRepository()
    saved_wallet = repo.save(core_wallet)

    # Verifica se a carteira foi atualizada corretamente
    updated_wallet = DjangoWallet.objects.get(cpf=user)
    assert saved_wallet.id == updated_wallet.id
    assert saved_wallet.balance == 300.0
    assert saved_wallet.last_transaction_date == timezone.localtime(updated_wallet.last_transaction_date)


@pytest.mark.django_db
def test_get_wallet_not_found():
    # Cria um usuário, mas não cria uma carteira
    CustomUser = get_user_model()
    user = CustomUser.objects.create(cpf="12345678909", name="Alice", password="senha123")

    # Testa o repositório
    repo = DjangoWalletRepository()
    with pytest.raises(DjangoWallet.DoesNotExist):
        repo.get_wallet("12345678909")