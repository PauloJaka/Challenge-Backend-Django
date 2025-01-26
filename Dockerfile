FROM python:3.10-slim

WORKDIR /app

# Copiar o arquivo de dependências para o container
COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]