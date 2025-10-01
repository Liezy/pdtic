#!/bin/bash

# Script de entrada para aguardar o banco de dados e executar migrations

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🐘 Aguardando PostgreSQL estar disponível...${NC}"

# Função para verificar se o banco está disponível
wait_for_postgres() {
    while ! python manage.py check --database default >/dev/null 2>&1; do
        echo -e "${YELLOW}⏳ Aguardando conexão com o banco de dados...${NC}"
        sleep 2
    done
    echo -e "${GREEN}✅ PostgreSQL está disponível!${NC}"
}

# Aguarda o banco estar disponível
wait_for_postgres

# Executa migrations
echo -e "${YELLOW}🔄 Executando migrations...${NC}"
python manage.py migrate

# Coleta arquivos estáticos
echo -e "${YELLOW}📦 Coletando arquivos estáticos...${NC}"
python manage.py collectstatic --noinput

# Cria superusuário se não existir
echo -e "${YELLOW}👤 Verificando superusuário...${NC}"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Criando superusuário admin/admin')
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin')
else:
    print('Superusuário já existe')
"

echo -e "${GREEN}🚀 Iniciando servidor Django...${NC}"

# Executa o comando passado como argumento ou runserver por padrão
exec "$@"