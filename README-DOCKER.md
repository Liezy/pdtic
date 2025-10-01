# 🐳 Docker Setup - PDTIC

Este projeto foi configurado para funcionar com Docker, especialmente para contornar limitações de redes institucionais.

## 📋 Arquivos Docker Criados

- `Dockerfile` - Containerização da aplicação Django
- `docker-compose.yml` - Configuração completa (Django + PostgreSQL)
- `docker-compose-db-only.yml` - Apenas PostgreSQL
- `run-postgres.sh` - Script para rodar PostgreSQL com network host
- `entrypoint.sh` - Script de inicialização automática
- `.dockerignore` - Otimização do build

## 🚀 Como Usar

### Opção 1: PostgreSQL no Docker + Django Local (Recomendado para redes institucionais)

```bash
# 1. Iniciar apenas o PostgreSQL
./run-postgres.sh

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Rodar migrations (se necessário)
python manage.py migrate

# 4. Iniciar Django
python manage.py runserver
```

### Opção 2: Tudo no Docker (se a rede permitir)

```bash
# Construir e iniciar todos os serviços
docker-compose up --build

# Ou em modo detached
docker-compose up --build -d
```

### Opção 3: Apenas PostgreSQL no Docker Compose

```bash
# Iniciar apenas o banco
docker-compose -f docker-compose-db-only.yml up -d

# Em seguida, rodar Django localmente
source venv/bin/activate
python manage.py runserver
```

## 🔧 Configurações

### Variáveis de Ambiente (.env)

O projeto usa as seguintes configurações para Docker:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=pdtic_db
DB_USER=pdtic_user
DB_PASSWORD=pdtic_password
DB_HOST=localhost  # ou 'db' para docker-compose
DB_PORT=5432
DEBUG=True
```

### Portas

- **Django**: `http://localhost:8000`
- **PostgreSQL**: `localhost:5432`

## 🛠 Comandos Úteis

```bash
# Ver logs do PostgreSQL
docker logs pdtic-postgres

# Parar PostgreSQL
docker stop pdtic-postgres

# Remover PostgreSQL
docker rm pdtic-postgres

# Conectar ao PostgreSQL
docker exec -it pdtic-postgres psql -U pdtic_user -d pdtic_db

# Ver containers rodando
docker ps

# Limpar tudo
docker-compose down --volumes --remove-orphans
```

## 🔍 Troubleshooting

### Problemas de Rede

Se você estiver em uma rede institucional e tiver problemas com `docker-compose`, use a **Opção 1** com o script `run-postgres.sh`.

### Erro de Build

Se o build falhar, tente:

```bash
# Limpar cache do Docker
docker system prune -f

# Rebuild sem cache
docker-compose build --no-cache
```

### Problemas de Permissão

```bash
# Tornar scripts executáveis
chmod +x run-postgres.sh entrypoint.sh
```

## 📦 Estrutura dos Containers

- **PostgreSQL**: Banco de dados principal
- **Django**: Aplicação web (quando usando docker-compose completo)
- **Volumes**: Persistência de dados do PostgreSQL

## 🎯 Próximos Passos

1. Acesse `http://localhost:8000` para verificar se está funcionando
2. Crie um superusuário: `python manage.py createsuperuser`
3. Acesse o admin: `http://localhost:8000/admin`

---

**Nota**: Para ambientes de produção, considere usar um banco PostgreSQL gerenciado ao invés de containers locais.