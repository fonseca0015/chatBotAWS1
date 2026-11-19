# Usar imagem oficial Python leve
FROM python:3.10-slim

# Evitar escrita de arquivos .pyc e garantir output direto no console
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências de sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta da Search API
EXPOSE 5000

# Comando para iniciar o servidor
CMD ["python", "main.py"]
