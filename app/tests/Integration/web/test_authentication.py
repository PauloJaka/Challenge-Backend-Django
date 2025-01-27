from django.urls import reverse
from rest_framework.test import APIClient
import pytest

@pytest.mark.django_db
def test_jwt_authentication():
    client = APIClient()
    
    user_data = {"name": "Alice", "cpf": "12345678909", "password": "senha123"}
    client.post(reverse("create_user"), data=user_data, format="json")
    
    auth_response = client.post(
        reverse("token_obtain_pair"),
        data={"cpf": "12345678909", "password": "senha123"},
        format="json"
    )
    
    access_token = auth_response.cookies.get("access_token")
    assert access_token is not None
    assert "HttpOnly" in str(access_token)  # Cookie seguro