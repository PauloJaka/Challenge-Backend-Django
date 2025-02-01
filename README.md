# Projeto Django Wallet API

## Visão Geral
Este projeto é uma API de carteira digital desenvolvida em Django, seguindo os princípios de **Clean Architecture** e utilizando **TDD (Test-Driven Development)** como padrão de design.

## Tecnologias Utilizadas
- **Django Rest Framework** (DRF) para criação da API
- **PostgreSQL** como banco de dados
- **Docker** e **Docker Compose** para conteinerização
- **JWT (JSON Web Token)** para autenticação
- **Flake8, Black, Isort** para linting e formatação de código
- **pytest** para testes automatizados

## Instalação e Execução
1. **Construir e subir os containers:**
   ```sh
   docker-compose up --build
   ```

2. **Entrar no container do backend:**
   ```sh
   docker exec -it nome_do_container_backend bash
   ```

3. **Popular o banco de dados com dados iniciais:**
   ```sh
   cd /app/modules/utils
   python populate_db.py
   ```

4. **Atualizar datas das transferências:**
   ```sh
   python update_transfer_dates.py
   ```

## Endpoints da API
### 1. **Criação de Usuário**
- **URL:** `POST /api/users/`
- **Entrada:**
  ```json
  {
    "name": "João Silva",
    "cpf": "12345678900",
    "password": "senha123"
  }
  ```
- **Resposta esperada:**
  ```json
  {
    "id": 1,
    "name": "João Silva",
    "cpf": "12345678900",
    "created_at": "2025-01-31T23:05:19.496-03:00"
  }
  ```

### 2. **Autenticação (JWT Token)**
- **URL:** `POST /api/token/`
- **Entrada:**
  ```json
  {
    "cpf": "12345678900",
    "password": "senha123"
  }
  ```
- **Resposta esperada:**
  ```json
  {
    "access": "<token_jwt>",
    "refresh": "<token_refresh>"
  }
  ```

### 3. **Atualizar Token JWT**
- **URL:** `POST /api/token/refresh/`
- **Entrada:**
  ```json
  {
    "refresh": "<token_refresh>"
  }
  ```
- **Resposta esperada:**
  ```json
  {
    "access": "<novo_token_jwt>"
  }
  ```

### 4. **Adicionar Saldo**
- **URL:** `POST /wallet/{cpf}/add_balance/`
- **Entrada:**
  ```json
  {
    "amount": 100.0
  }
  ```
- **Resposta esperada:**
  ```json
  {
    "balance": 100.0
  }
  ```

### 5. **Transferência de Fundos**
- **URL:** `POST /wallet/transfer/`
- **Entrada:**
  ```json
  {
    "target_cpf": "98765432100",
    "amount": 50.0
  }
  ```
- **Resposta esperada:**
  ```json
  {
    "message": "Transferência realizada com sucesso."
  }
  ```

### 6. **Consultar Saldo**
- **URL:** `GET /api/wallet/balance/`
- **Resposta esperada:**
  ```json
  {
    "balance": 50.0
  }
  ```

### 7. **Listar Transferências**
- **URL:** `GET /wallet/transfers/`
- **Resposta esperada:**
  ```json
  [
    {
      "id": 1,
      "source_cpf": "12345678900",
      "target_cpf": "98765432100",
      "amount": 50.0,
      "date": "2025-01-31T23:05:19.496-03:00"
    }
  ]
  ```

## Estrutura do Projeto
```
/app
  ├── modules
  │   ├── utils
  │   │   ├── populate_db.py  # Popula o banco de dados
  │   │   ├── update_transfer_dates.py  # Atualiza datas das transferências
  │   ├── application
  │   │   ├── use_cases  # Casos de uso
  │   ├── domain
  │   │   ├── entities  # Entidades do domínio
  │   │   ├── exceptions  # Exceções personalizadas
  │   ├── infrastructure
  │   │   ├── models.py  # Modelos Django
  │   │   ├── repositories  # Repositórios de acesso a dados
  │   │   ├── settings.py  # Configurações Django
  │   ├── webapps
  │   │   ├── views.py  # Views da API
  ├── docker-compose.yml  # Configuração dos containers
  ├── Dockerfile  # Configuração do backend
  ├── requirements.txt  # Dependências do projeto
  ├── manage.py  # Gerenciamento do Django
```

## Testes
Para rodar os testes automatizados:
```sh
pytest
```

## Estilo de Código
O projeto segue as regras de linting com:
- **Flake8** para verificação de estilo
- **Black** para formatação de código
- **Isort** para organização de importações

Para aplicar automaticamente:
```sh
black . && isort . && flake8
```

## Considerações Finais
O projeto foi desenvolvido utilizando **Clean Architecture**, garantindo separação clara entre camadas de aplicação, domínio e infraestrutura. Caso precise de melhorias ou novas features, sinta-se à vontade para contribuir!

---
🚀 **Desenvolvido com Django + DRF + Clean Architecture**

