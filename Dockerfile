# Use Python 3.10 como base
FROM python:3.10-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema em uma única camada
RUN apt-get update && apt-get install -y \
        postgresql-client \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia e instala as dependências Python (versão minimal)
COPY requirements-minimal.txt /app/
RUN pip install --no-cache-dir -r requirements-minimal.txt

# Copia o código da aplicação
COPY . /app/

# Torna o script executável
RUN chmod +x /app/entrypoint.sh

# Cria um usuário não-root para segurança
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
    && chown -R user:user /app
USER user

# Expõe a porta 8000
EXPOSE 8000

# Define o entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando padrão para iniciar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]