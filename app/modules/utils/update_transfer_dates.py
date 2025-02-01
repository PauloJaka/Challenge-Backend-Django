import psycopg2

# Configurações do banco de dados
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"  # Substitua pela senha do PostgreSQL
DB_HOST = "db"            # Nome do serviço no docker-compose.yml
DB_PORT = "5432"

# Conectar ao banco de dados
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Ler o arquivo SQL
with open('update_transfer_dates.sql', 'r') as file:
    sql_script = file.read()

# Executar o script SQL
cursor.execute(sql_script)

# Commit e fechar a conexão
conn.commit()
conn.close()

print("Datas das transferências atualizadas com sucesso!")