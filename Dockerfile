# Imagem base leve compatível com Lambda (Python 3.9)
FROM python:3.9-slim

# Diretório de trabalho
WORKDIR /app

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .
COPY requirements-dev.txt .

# Instalar dependências do projeto e de desenvolvimento
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Copiar código fonte
COPY src/ src/
COPY local_server.py .

# Expor porta padrão do FastAPI/Uvicorn
EXPOSE 8000

# Criar usuário não-root para segurança
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Comando de inicialização com hot-reload habilitado
CMD ["uvicorn", "local_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
