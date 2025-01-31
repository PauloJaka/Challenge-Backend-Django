import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from infrastructure.models.transfer_model import DjangoTransfer
import logging

@pytest.fixture
def create_transfer():
    def _create_transfer(source_cpf, target_cpf, amount, date=None):
        from infrastructure.models.transfer_model import DjangoTransfer
        return DjangoTransfer.objects.create(
            source_cpf=source_cpf,
            target_cpf=target_cpf,
            amount=amount,
            date=date or timezone.now()
        )
    return _create_transfer

@pytest.mark.django_db(transaction=True)
def test_list_transfers_with_data(create_transfer, caplog):
    # Enable debug logging
    caplog.set_level(logging.DEBUG)
    
    client = APIClient()
    
    # Create and authenticate user
    user_response = client.post(reverse("create_user"), {
        "cpf": "12345678909",
        "name": "Alice",
        "password": "senha123"
    })
    print(f"User creation response: {user_response.status_code}")
    
    auth_response = client.post(reverse("token_obtain_pair"), {
        "cpf": "12345678909",
        "password": "senha123"
    })
    token = auth_response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    transfer1 = create_transfer("12345678909", "98765432100", 100.0)
    transfer2 = create_transfer("12345678909", "98765432100", 200.0)
    
    transfers_in_db = DjangoTransfer.objects.all()
    print(f"Number of transfers in DB: {transfers_in_db.count()}")
    for transfer in transfers_in_db:
        print(f"Transfer in DB: ID={transfer.id}, Source={transfer.source_cpf}, Amount={transfer.amount}")
    
    response = client.get(reverse("list_transfers"))
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.content.decode()}")
    
    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}. "
        f"Response content: {response.content.decode()}"
    )
    
    # Only continue with these assertions if we get a 200 status
    if response.status_code == 200:
        response_data = response.json()
        transfers = response_data.get("results", [])
        assert len(transfers) == 2, f"Expected 2 transfers, got {len(transfers)}"



@pytest.mark.django_db(transaction=True)
def test_list_transfers_no_data(create_transfer):
    client = APIClient()

    # Create and authenticate user
    client.post(reverse("create_user"), {
        "cpf": "12345678909", 
        "name": "Alice", 
        "password": "senha123"
    })
    auth_response = client.post(reverse("token_obtain_pair"), {
        "cpf": "12345678909", 
        "password": "senha123"
    })
    token = auth_response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Não cria transferências para o usuário

    response = client.get(reverse("list_transfers"))
    assert response.status_code == 404  # Verifica se retorna 404 quando não há transferências
    assert response.json() == {"message": "No transfers found"}  # Verifica a mensagem

@pytest.mark.django_db(transaction=True)
def test_list_transfers_empty_filtered(create_transfer):
    client = APIClient()

    # Create and authenticate user
    client.post(reverse("create_user"), {
        "cpf": "12345678909", 
        "name": "Alice", 
        "password": "senha123"
    })
    auth_response = client.post(reverse("token_obtain_pair"), {
        "cpf": "12345678909", 
        "password": "senha123"
    })
    token = auth_response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Cria test transfers
    create_transfer("12345678909", "98765432100", 100.0)
    create_transfer("12345678909", "98765432100", 200.0)

    # Faz uma requisição com um filtro que não vai retornar nada
    response = client.get(reverse("list_transfers") + "?start_date=2023-01-01&end_date=2023-01-02")
    assert response.status_code == 404  # Espera-se 404 se não houver transferências para esse filtro
    assert response.json() == {"message": "No transfers found"}

