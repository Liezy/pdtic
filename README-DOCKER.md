# 🐳 Sistema PDTIC - Guia Completo de Docker

Este guia ensina como executar o sistema PDTIC completo usando Docker, desde a configuração inicial até comandos avançados para manutenção e solução de problemas.

## 📋 Pré-requisitos

- **Docker** (versão 20.10 ou superior)
- **Docker Compose** (versão 1.29 ou superior)
- Pelo menos **4GB de RAM** disponível
- **2GB de espaço em disco** livre

### Verificar instalação do Docker

```bash
# Verificar se Docker está instalado e funcionando
docker --version
docker-compose --version

# Testar Docker
docker run hello-world
```

## 🚀 Executando o Sistema PDTIC

### Sistema Completo (Recomendado)

```bash
# 1. Clonar o repositório (se ainda não fez)
git clone <url-do-repositorio>
cd pdtic

# 2. Construir e iniciar todos os serviços
docker-compose up --build

# Ou em modo detached (background)
docker-compose up --build -d
```

## 🌐 Acessando o Sistema

Após iniciar os containers, acesse:

- **Aplicação Web**: http://localhost:8000
- **Banco PostgreSQL**: localhost:5432
  - Usuário: `pdtic_user`
  - Senha: `pdtic_password`
  - Database: `pdtic_db`

## 🛠 Comandos Essenciais do Docker

### Gerenciamento de Containers

```bash
# Ver containers em execução
docker ps

# Ver todos os containers (incluindo parados)
docker ps -a

# Ver logs de um container específico
docker-compose logs web
docker-compose logs db

# Acessar shell de um container em execução
docker-compose exec web bash
docker-compose exec db bash

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (ATENÇÃO: perde dados!)
docker-compose down --volumes --remove-orphans
```

### Gerenciamento de Imagens

```bash
# Ver imagens locais
docker images

# Remover imagem não utilizada
docker image rm pdtic_web:latest

# Limpar imagens não utilizadas
docker image prune -f

# Ver espaço usado pelo Docker
docker system df
```

### Limpeza e Manutenção

```bash
# Limpar containers parados
docker container prune -f

# Limpar volumes não utilizados
docker volume prune -f

# Limpar rede não utilizadas
docker network prune -f

# Limpeza geral (containers, redes, imagens dangling)
docker system prune -f

# Limpeza completa (inclui volumes - CUIDADO!)
docker system prune --volumes -f
```

### Comandos Avançados

```bash
# Executar comando em container específico
docker-compose exec web python manage.py shell
docker-compose exec db psql -U pdtic_user -d pdtic_db

# Copiar arquivos do/para container
docker cp arquivo.txt pdtic_web_1:/app/
docker cp pdtic_web_1:/app/arquivo.txt .

# Ver estatísticas de uso de recursos
docker stats

# Inspecionar detalhes de um container
docker inspect pdtic_web_1

# Ver logs em tempo real
docker-compose logs -f web
```

## 🔧 Solução de Problemas

### Problema: Porta já em uso

```bash
# Verificar qual processo está usando a porta
sudo lsof -i :5432
sudo lsof -i :8000

# Matar processo usando a porta
sudo kill -9 <PID>

# Ou parar serviço do sistema
sudo systemctl stop postgresql
```

### Problema: Container não inicia

```bash
# Ver logs detalhados
docker-compose logs

# Reconstruir sem cache
docker-compose build --no-cache

# Verificar se há conflitos de nomes
docker-compose down
docker-compose up --build
```

### Problema: Erro de conexão com banco

```bash
# Verificar se o container do banco está rodando
docker-compose ps

# Testar conectividade
docker-compose exec web nc -z db 5432

# Verificar variáveis de ambiente
docker-compose exec web env | grep DB_
```

### Problema: Migrações não aplicadas

```bash
# Aplicar migrações manualmente
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Coletar arquivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

### Problema: Memória insuficiente

```bash
# Verificar uso de memória
docker stats

# Aumentar limite de memória do Docker Desktop
# Ou liberar memória do sistema
docker system prune --volumes -f
```

## 📁 Estrutura dos Containers

```
pdtic/
├── docker-compose.yml          # Configuração dos serviços
├── Dockerfile                  # Instruções para construir a imagem Django
├── requirements-minimal.txt    # Dependências essenciais
├── entrypoint.sh              # Script de inicialização
├── .env                       # Variáveis de ambiente
└── core/                      # Código da aplicação Django
    ├── settings.py
    ├── urls.py
    └── ...
```

### Volumes Persistentes

- **postgres_data**: Dados do PostgreSQL
- **static_volume**: Arquivos estáticos coletados

## 🔒 Segurança

### Para Produção

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  db:
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}  # Usar variável de ambiente
    volumes:
      - ./backups:/backups  # Para backups

  web:
    environment:
      DEBUG: 'False'
      SECRET_KEY: ${SECRET_KEY}
      ALLOWED_HOSTS: ${ALLOWED_HOSTS}
```

### Variáveis de Ambiente Seguras

```bash
# Criar arquivo .env seguro
echo "SECRET_KEY=your-secret-key-here" > .env
echo "DB_PASSWORD=secure-password" >> .env

# Nunca commite .env no Git
echo ".env" >> .gitignore
```

## 📊 Monitoramento

```bash
# Ver logs em tempo real
docker-compose logs -f

# Monitorar recursos
docker stats pdtic_web_1 pdtic_db_1

# Verificar saúde dos serviços
curl http://localhost:8000/health/  # Se implementar endpoint de saúde
```

## 🚀 Deploy em Produção

### Usando Docker Swarm

```bash
# Inicializar swarm
docker swarm init

# Deploy da stack
docker stack deploy -c docker-compose.yml pdtic

# Ver serviços
docker stack services pdtic
```

### Usando Kubernetes

```yaml
# kubernetes/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pdtic-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pdtic-web
  template:
    metadata:
      labels:
        app: pdtic-web
    spec:
      containers:
      - name: web
        image: pdtic_web:latest
        ports:
        - containerPort: 8000
```

## 🎯 Comandos de Desenvolvimento

```bash
# Executar testes
docker-compose exec web python manage.py test

# Criar nova migração
docker-compose exec web python manage.py makemigrations

# Ver shell do Django
docker-compose exec web python manage.py shell

# Verificar sintaxe
docker-compose exec web python manage.py check
```

## 📚 Recursos Adicionais

- [Documentação Oficial do Docker](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django + Docker Best Practices](https://docs.docker.com/samples/django/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)

## ❓ FAQ

**P: Como atualizar o código da aplicação?**
```bash
docker-compose down
git pull
docker-compose up --build
```

**P: Como fazer backup do banco?**
```bash
docker-compose exec db pg_dump -U pdtic_user pdtic_db > backup.sql
```

**P: Como restaurar backup?**
```bash
docker-compose exec -T db psql -U pdtic_user pdtic_db < backup.sql
```

**P: Como escalar a aplicação?**
```bash
docker-compose up -d --scale web=3
```

---

**Nota**: Este guia assume que você está familiarizado com conceitos básicos de Django. Para dúvidas específicas da aplicação PDTIC, consulte a documentação do projeto.
