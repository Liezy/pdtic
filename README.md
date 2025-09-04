# PDTIC

Sistema web desenvolvido em Django para gestão de instituições e funcionalidades relacionadas.

## Funcionalidades
- Cadastro, edição e exclusão de instituições
- Página inicial personalizada
- Estrutura pronta para novos módulos

## Requisitos
- Python 3.12+
- Django 4.x+

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/Liezy/pdtic.git
   ```
2. Acesse a pasta do projeto:
   ```bash
   cd pdtic
   ```
3. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Execução
1. Realize as migrações:
   ```bash
   python manage.py migrate
   ```
2. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```
3. Acesse o sistema em: http://localhost:8000/

## Estrutura do Projeto
- `core/` - Configurações principais do Django
- `home/` - Página inicial e funcionalidades básicas
- `instituicoes/` - Módulo de instituições
- `templates/` - Templates HTML

## Contribuição
Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro para discutir o que deseja modificar.

## Licença
Este projeto está sob a licença MIT.
