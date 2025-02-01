from django.urls import reverse
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
def test_get_wallet_balance_authenticated():
    client = APIClient()

    # 1. Cria um usuário
    user_data = {"cpf": "12345678909", "name": "Alice", "password": "senha123"}
    client.post(reverse("create_user"), user_data, format="json")

    # 2. Autentica o usuário para obter o token JWT
    auth_response = client.post(
        reverse("token_obtain_pair"),
        {"cpf": "12345678909", "password": "senha123"},
        format="json",
    )

    # Verifica se a autenticação foi bem-sucedida
    assert auth_response.status_code == 200
    access_token = auth_response.data["access"]

    # 3. Passa o token JWT no cabeçalho da requisição
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # 4. Consulta o saldo
    response = client.get(reverse("wallet_balance"))

    # Verifica a resposta
    assert response.status_code == 200
    assert "balance" in response.json()


@pytest.mark.django_db
def test_get_wallet_balance_unauthenticated():
    client = APIClient()
    response = client.get(reverse("wallet_balance"))
    assert response.status_code == 401  # Não autenticado
