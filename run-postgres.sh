#!/bin/bash

# Script para rodar PostgreSQL com Docker usando network host
# Isso contorna problemas de rede em ambientes restritivos

echo "🐘 Parando containers PostgreSQL existentes..."
docker stop pdtic-postgres 2>/dev/null || true
docker rm pdtic-postgres 2>/dev/null || true

echo "🚀 Iniciando PostgreSQL com network host..."
docker run -d \
  --name pdtic-postgres \
  --network host \
  -e POSTGRES_DB=pdtic_db \
  -e POSTGRES_USER=pdtic_user \
  -e POSTGRES_PASSWORD=pdtic_password \
  -v pdtic_postgres_data:/var/lib/postgresql/data \
  postgres:13

echo "⏳ Aguardando PostgreSQL inicializar..."
sleep 5

echo "✅ PostgreSQL está rodando na porta 5432"
echo "📋 Para conectar:"
echo "   Host: localhost"
echo "   Port: 5432" 
echo "   Database: pdtic_db"
echo "   User: pdtic_user"
echo "   Password: pdtic_password"

echo ""
echo "🛑 Para parar: docker stop pdtic-postgres"
echo "🔄 Para ver logs: docker logs pdtic-postgres"