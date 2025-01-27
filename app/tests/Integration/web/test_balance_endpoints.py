@pytest.mark.django_db
def test_get_balance_authenticated():
    client = APIClient()

    # Cria usuário e autentica
    client.post(
        reverse("create_user"),
        data={"name": "Alice", "cpf": "12345678909", "password": "senha123"},
    )
    auth_response = client.post(
        reverse("token_obtain_pair"),
        data={"cpf": "12345678909", "password": "senha123"},
    )
    client.cookies = auth_response.cookies

    # Consulta saldo
    response = client.get(reverse("get_balance"))
    assert response.status_code == 200
    assert response.json() == {"balance": 0.0}
