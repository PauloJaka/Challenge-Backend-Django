import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from infrastructure.models.wallet_model import DjangoWallet
from django.contrib.auth import get_user_model
from decimal import Decimal

@pytest.mark.django_db
def test_add_balance_to_wallet():
    cpf = "12345678909"
    user = get_user_model().objects.create(cpf=cpf)
    wallet = DjangoWallet.objects.create(cpf=user, balance=Decimal('100.0'))

    client = APIClient()

    response = client.post(reverse('add_balance_to_wallet', kwargs={"cpf": cpf}), data={'amount': 50.0})

    assert response.status_code == status.HTTP_200_OK

    wallet.refresh_from_db()  
    assert wallet.balance == Decimal('150.0')  

@pytest.mark.django_db
def test_add_balance_negative_amount():
    cpf = "12345678909"
    user = get_user_model().objects.create(cpf=cpf)
    wallet = DjangoWallet.objects.create(cpf=user, balance=Decimal('100.0'))

    client = APIClient()

    # Enviando o valor negativo
    response = client.post(reverse('add_balance_to_wallet', kwargs={"cpf": cpf}), data={'amount': -50.0})

    # Acessando a resposta JSON corretamente
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "A quantidade a ser adicionada deve ser positiva" in response.json()["error"]



@pytest.mark.django_db
def test_wallet_not_found():
    # CPF que não existe
    cpf = "00000000000"
    
    # Criando um cliente de API
    client = APIClient()
    
    # Chamando o endpoint para CPF não existente
    response = client.post(reverse('add_balance_to_wallet', kwargs={"cpf": cpf}), data={'amount': 50.0})

    # Verificando se a resposta de erro foi correta
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Carteira não encontrada" in response.json()["error"]

