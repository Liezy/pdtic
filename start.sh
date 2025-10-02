#!/bin/bash

# Script para iniciar o projeto Django com Docker sem problemas de rede

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Iniciando projeto Django PDTIC...${NC}"

# Função para limpeza inteligente apenas quando necessário
cleanup_if_needed() {
    if docker compose ps | grep -q "Exit\|Dead"; then
        echo -e "${YELLOW}⚠️  Containers em estado inconsistente detectados. Fazendo limpeza...${NC}"
        docker compose down --remove-orphans
        docker network prune -f > /dev/null 2>&1
        return 0
    fi
    
    # Verifica se há conflito de rede
    if ! docker compose config > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Conflito de rede detectado. Fazendo limpeza...${NC}"
        docker compose down --remove-orphans > /dev/null 2>&1
        docker network prune -f > /dev/null 2>&1
        return 0
    fi
    
    return 1
}

# Verifica se precisa fazer limpeza
if cleanup_if_needed; then
    echo -e "${GREEN}✅ Limpeza concluída.${NC}"
fi

# Inicia os serviços usando Docker Compose V2
echo -e "${BLUE}🚀 Iniciando containers...${NC}"

if [ "$1" = "--build" ]; then
    echo -e "${YELLOW}🔨 Rebuild solicitado...${NC}"
    docker compose up --build
elif [ "$1" = "-d" ] || [ "$1" = "--detach" ]; then
    echo -e "${BLUE}🌐 Iniciando em modo background...${NC}"
    docker compose up -d
    echo -e "${GREEN}✅ Containers iniciados em background!${NC}"
    echo -e "${BLUE}📱 Aplicação: http://localhost:8000${NC}"
    echo -e "${BLUE}🔧 Admin: http://localhost:8000/admin (admin/admin)${NC}"
    echo -e "${BLUE}📊 Para ver logs: docker compose logs -f${NC}"
    echo -e "${BLUE}🛑 Para parar: docker compose down${NC}"
else
    docker compose up
fi