import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from infrastructure.models import DjangoTransfer  # Ajuste o import para seu app


@pytest.fixture
def create_transfer():
    def _create_transfer(source_cpf, target_cpf, amount, date=None):
        if date is None:
            date = timezone.localtime()

        transfer = DjangoTransfer.objects.create(
            source_cpf=source_cpf, target_cpf=target_cpf, amount=amount, date=date
        )
        return transfer

    return _create_transfer


@pytest.mark.django_db(transaction=True)
def test_list_transfers_with_data(create_transfer):
    client = APIClient()

    user_response = client.post(
        reverse("create_user"),
        {"cpf": "12345678909", "name": "Alice", "password": "senha123"},
    )
    print(f"User creation response: {user_response.content}")

    auth_response = client.post(
        reverse("token_obtain_pair"), {"cpf": "12345678909", "password": "senha123"}
    )
    token = auth_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    transfer1 = create_transfer("12345678909", "98765432100", 100.0)
    transfer2 = create_transfer("12345678909", "98765432100", 200.0)

    print(f"Transfer 1: {transfer1.id}, Transfer 2: {transfer2.id}")

    response = client.get(reverse("list_transfers"))
    print(f"Response content: {response.content}")

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}, content: {response.content}"

    transfers = response.json().get("results", [])
    assert len(transfers) == 2, f"Expected 2 transfers, got {len(transfers)}"


@pytest.mark.django_db(transaction=True)
def test_list_transfers_no_data(create_transfer):
    client = APIClient()

    # Criação do usuário
    client.post(
        reverse("create_user"),
        {"cpf": "12345678909", "name": "Alice", "password": "senha123"},
    )

    # Autenticação
    auth_response = client.post(
        reverse("token_obtain_pair"), {"cpf": "12345678909", "password": "senha123"}
    )
    token = auth_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.get(reverse("list_transfers"))
    assert response.status_code == 204
    assert response.content == b""


@pytest.mark.django_db(transaction=True)
def test_list_transfers_empty_filtered(create_transfer):
    client = APIClient()

    client.post(
        reverse("create_user"),
        {"cpf": "12345678909", "name": "Alice", "password": "senha123"},
    )

    # Autenticação
    auth_response = client.post(
        reverse("token_obtain_pair"), {"cpf": "12345678909", "password": "senha123"}
    )
    token = auth_response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    create_transfer("12345678909", "98765432100", 100.0)
    create_transfer("12345678909", "98765432100", 200.0)

    response = client.get(
        reverse("list_transfers") + "?start_date=2023-01-01&end_date=2023-01-02"
    )
    assert response.status_code == 204
    assert response.content == b""
