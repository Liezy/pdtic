#!/bin/bash

# Script para limpeza rápida do Docker quando houver problemas

echo "🧹 Fazendo limpeza completa do Docker..."

# Para todos os containers do projeto
docker compose down --remove-orphans > /dev/null 2>&1

# Remove redes órfãs
docker network prune -f > /dev/null 2>&1

# Remove volumes órfãos (opcional - descomente se necessário)
# docker volume prune -f > /dev/null 2>&1

# Remove containers parados
docker container prune -f > /dev/null 2>&1

echo "✅ Limpeza concluída! Agora você pode executar:"
echo "   ./start.sh          # Para iniciar normalmente"
echo "   ./start.sh -d       # Para iniciar em background"
echo "   ./start.sh --build  # Para rebuild completo"