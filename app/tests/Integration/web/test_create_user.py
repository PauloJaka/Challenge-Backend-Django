import pytest
from django.utils import timezone
from application.use_cases.create_user import CreateUserUseCase
from infrastructure.repositories.django_user_repository import DjangoUserRepository
from infrastructure.repositories.django_wallet_repository import DjangoWalletRepository
from domain.entities.user import User
from domain.entities.wallet import Wallet

from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_create_user_with_wallet_integration():
    # Repositórios reais (não mocks)
    user_repo = DjangoUserRepository()
    wallet_repo = DjangoWalletRepository()

    use_case = CreateUserUseCase(user_repo, wallet_repo)

    # Dados de teste
    name = "Bob"
    cpf = "98765432100"
    password = "senha456"

    returned_user = use_case.execute(name, cpf, password)

    saved_user = user_repo.get_by_cpf(cpf)
    assert saved_user is not None
    assert saved_user.name == name
    assert saved_user.cpf == cpf

    user_model = get_user_model()
    django_user = user_model.objects.get(cpf=cpf)
    assert django_user.check_password(password)  # Verifica se a senha fornecida corresponde ao hash

    saved_wallet = wallet_repo.get_wallet(cpf) 
    assert saved_wallet is not None
    assert saved_wallet.cpf == cpf
    assert saved_wallet.balance == 0.0  
    assert isinstance(saved_wallet, Wallet)

