from django.urls import reverse
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
def test_jwt_authentication():
    client = APIClient()

    user_data = {"name": "Alice", "cpf": "12345678909", "password": "senha123"}
    create_response = client.post(reverse("create_user"), data=user_data, format="json")

    assert create_response.status_code == 201

    auth_response = client.post(
        reverse("token_obtain_pair"),
        data={"cpf": "12345678909", "password": "senha123"},
        format="json",
    )

    print("Resposta da autenticação JWT:", auth_response.json())

    # Verificar se o token foi gerado corretamente
    access_token = auth_response.json().get("access")
    assert access_token is not None  # Verifica se o token de acesso foi gerado
