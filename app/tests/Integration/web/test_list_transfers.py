import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone

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
def test_list_transfers(create_transfer):
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

    # Create test transfers
    create_transfer("12345678909", "98765432100", 100.0)
    create_transfer("12345678909", "98765432100", 200.0)

    response = client.get(reverse("list_transfers"))
    assert response.status_code == 200
    transfers = response.json()
    assert len(transfers) == 2