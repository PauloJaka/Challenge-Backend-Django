import json
import requests
from datetime import datetime

# Configurações
BASE_URL = "http://localhost:8000"  # URL base da sua API
JSON_FILE_PATH = "fixtures/initial_data.json"  # Caminho para o arquivo JSON

# Endpoints
CREATE_USER_URL = f"{BASE_URL}/api/users/"
TOKEN_OBTAIN_URL = f"{BASE_URL}/api/token/"
ADD_BALANCE_URL = f"{BASE_URL}/wallet/<str:cpf>/add_balance/"
TRANSFER_FUNDS_URL = f"{BASE_URL}/wallet/transfer/"
UPDATE_TRANSFER_URL = (
    f"{BASE_URL}/wallet/transfer/<int:pk>/"  # Endpoint para atualizar transferências
)


# Função para obter token JWT
def get_jwt_token(cpf, password):
    payload = {
        "cpf": cpf,
        "password": password,
    }
    response = requests.post(TOKEN_OBTAIN_URL, json=payload)
    if response.status_code == 200:
        return response.json()["access"]
    else:
        print(
            f"Erro ao obter token para o usuário {cpf}: {response.status_code} - {response.text}"
        )
        return None


# Função para criar usuários
def create_user(user_data):
    payload = {
        "name": user_data["name"],
        "cpf": user_data["cpf"],
        "password": user_data["password"],
    }
    response = requests.post(CREATE_USER_URL, json=payload)
    if response.status_code == 201:
        print(f"Usuário criado: {user_data['cpf']}")
    else:
        print(
            f"Erro ao criar usuário {user_data['cpf']}: {response.status_code} - {response.text}"
        )


# Função para adicionar saldo à carteira
def add_balance_to_wallet(wallet_data):
    cpf = wallet_data["cpf"]
    balance = float(wallet_data["balance"])

    # Verifica se o saldo é positivo
    if balance <= 0:
        print(f"Erro: Saldo inválido para o usuário {cpf}. O saldo deve ser positivo.")
        return

    payload = {
        "amount": balance,  # Certifique-se de que o campo esperado é "amount" e não "balance"
    }
    url = ADD_BALANCE_URL.replace("<str:cpf>", cpf)
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Saldo adicionado para o usuário {cpf}")
    else:
        print(
            f"Erro ao adicionar saldo para o usuário {cpf}: {response.status_code} - {response.text}"
        )


# Função para criar transferências
def create_transfer(transfer_data, token):
    payload = {
        "source_cpf": transfer_data["source_cpf"],
        "target_cpf": transfer_data["target_cpf"],
        "amount": float(transfer_data["amount"]),
    }
    headers = {
        "Authorization": f"Bearer {token}",
    }
    response = requests.post(TRANSFER_FUNDS_URL, json=payload, headers=headers)
    if response.status_code == 201:
        print(
            f"Transferência criada: {transfer_data['source_cpf']} -> {transfer_data['target_cpf']}"
        )
        return response.json()  # Retorna os dados da transferência criada
    else:
        print(f"transferência: {response.status_code} - {response.text}")
        return None


# Função para atualizar a data da transferência
def update_transfer_date(transfer_id, date, token):
    payload = {
        "date": date,  # Passa a data do JSON
    }
    headers = {
        "Authorization": f"Bearer {token}",
    }
    url = UPDATE_TRANSFER_URL.replace("<int:pk>", str(transfer_id))
    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Data da transferência {transfer_id} atualizada para {date}")
    else:
        print(
            f"Erro ao atualizar data da transferência {transfer_id}: {response.status_code} - {response.text}"
        )


# Função principal para processar o JSON
def process_json(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)

    # Criar usuários
    for item in data:
        if item["model"] == "infrastructure.customuser":
            create_user(item["fields"])

    # Adicionar saldo às carteiras
    for item in data:
        if item["model"] == "infrastructure.djangoWallet":
            add_balance_to_wallet(item["fields"])

    # Criar transferências (requer autenticação)
    for item in data:
        if item["model"] == "infrastructure.djangotransfer":
            # Obtém o token JWT para o usuário que está realizando a transferência
            source_cpf = item["fields"]["source_cpf"]
            user_data = next(
                user
                for user in data
                if user["model"] == "infrastructure.customuser"
                and user["fields"]["cpf"] == source_cpf
            )
            token = get_jwt_token(source_cpf, user_data["fields"]["password"])

            if token:
                # Cria a transferência
                transfer_response = create_transfer(item["fields"], token)
                if transfer_response:
                    # Atualiza a data da transferência
                    transfer_id = transfer_response[
                        "id"
                    ]  # Supondo que o endpoint retorne o ID da transferência
                    update_transfer_date(transfer_id, item["fields"]["date"], token)


# Executar o script
if __name__ == "__main__":
    process_json(JSON_FILE_PATH)
