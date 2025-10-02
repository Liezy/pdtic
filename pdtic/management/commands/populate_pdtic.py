from django.core.management.base import BaseCommand
from pdtic.models import PDTIC, VersaoPDTIC
from instituicoes.models import Instituicao
from datetime import date

class Command(BaseCommand):
    help = 'Popula o banco de dados com PDTICs e suas versões de exemplo'

    def handle(self, *args, **options):
        # Obter instituições existentes
        instituicoes = Instituicao.objects.all()
        if not instituicoes:
            self.stdout.write(self.style.ERROR('Nenhuma instituição encontrada. Execute primeiro o comando populate_instituicoes.'))
            return

        # Dados realistas de PDTICs para órgãos públicos brasileiros
        pdtic_data = [
            {
                'titulo': 'PDTIC 2024-2027 - Transformação Digital do Sistema Tributário',
                'descricao': 'Plano para modernização da infraestrutura tecnológica da Receita Federal, implementação de sistemas de inteligência artificial para análise fiscal e ampliação dos serviços digitais aos contribuintes. Inclui migração para nuvem governamental e fortalecimento da segurança cibernética.',
                'vigencia_inicio': date(2024, 1, 1),
                'vigencia_fim': date(2027, 12, 31),
                'status': 'publicado',
                'versoes': [
                    {'numero_versao': '1.0', 'data_aprovacao': date(2023, 11, 30), 'observacoes': 'Versão inicial aprovada pelo Comitê de TI.'},
                    {'numero_versao': '1.1', 'data_aprovacao': date(2024, 6, 15), 'observacoes': 'Revisão para adequação à Lei Geral de Proteção de Dados.'},
                ],
            },
            {
                'titulo': 'PDTIC 2025-2029 - Auditoria Digital e Controle Social',
                'descricao': 'Estratégia de modernização dos processos de auditoria e controle através de ferramentas de análise de dados, implementação de trilhas de auditoria automatizadas e desenvolvimento de portais de transparência com dados abertos para controle social.',
                'vigencia_inicio': date(2025, 1, 1),
                'vigencia_fim': date(2029, 12, 31),
                'status': 'aprovado',
                'versoes': [
                    {'numero_versao': '1.0', 'data_aprovacao': date(2024, 10, 25), 'observacoes': 'Plano aprovado com foco em Big Data e Analytics.'},
                ],
            },
            {
                'titulo': 'PDTIC 2024-2028 - Sistema Financeiro Nacional Digital',
                'descricao': 'Implementação do Real Digital (CBDC), modernização do Sistema de Pagamentos Brasileiros (SPB), desenvolvimento de APIs para Open Banking e fortalecimento da supervisão tecnológica das instituições financeiras através de RegTech e SupTech.',
                'vigencia_inicio': date(2024, 1, 1),
                'vigencia_fim': date(2028, 12, 31),
                'status': 'elaboracao',
                'versoes': [
                    {'numero_versao': '0.9', 'data_aprovacao': date(2024, 8, 20), 'observacoes': 'Versão em consulta pública até dezembro/2024.'},
                ],
            },
            {
                'titulo': 'PDTIC 2023-2026 - Digitalização da Previdência Social',
                'descricao': 'Modernização completa dos sistemas previdenciários com foco na experiência do usuário, implementação de atendimento por chatbot com IA, digitalização total do acervo documental e integração com bases de dados governamentais para concessão automática de benefícios.',
                'vigencia_inicio': date(2023, 1, 1),
                'vigencia_fim': date(2026, 12, 31),
                'status': 'publicado',
                'versoes': [
                    {'numero_versao': '1.0', 'data_aprovacao': date(2022, 12, 10), 'observacoes': 'Plano inicial focado em digitalização de processos.'},
                    {'numero_versao': '2.0', 'data_aprovacao': date(2024, 3, 22), 'observacoes': 'Revisão maior incorporando IA e análise preditiva.'},
                ],
            },
            {
                'titulo': 'PDTIC 2024-2027 - Governo Transparente e Íntegro',
                'descricao': 'Desenvolvimento de plataformas de transparência ativa, implementação de sistemas de detecção de fraudes baseados em machine learning, criação de painéis de controle social em tempo real e modernização dos canais de ouvidoria com análise de sentimento.',
                'vigencia_inicio': date(2024, 1, 1),
                'vigencia_fim': date(2027, 12, 31),
                'status': 'aprovado',
                'versoes': [
                    {'numero_versao': '1.0', 'data_aprovacao': date(2023, 12, 15), 'observacoes': 'Aprovado com foco em transparência e participação social.'},
                ],
            },
            {
                'titulo': 'PDTIC 2025-2028 - Telecomunicações 5G e Conectividade',
                'descricao': 'Regulamentação e fiscalização da implementação do 5G no Brasil, desenvolvimento de sistemas de monitoramento da qualidade de serviços em tempo real, modernização dos processos de outorga de radiofrequências e criação de laboratórios de testes para IoT.',
                'vigencia_inicio': date(2025, 1, 1),
                'vigencia_fim': date(2028, 12, 31),
                'status': 'rascunho',
                'versoes': [
                    {'numero_versao': '0.5', 'data_aprovacao': date(2024, 9, 10), 'observacoes': 'Versão preliminar em elaboração pela equipe técnica.'},
                ],
            },
            {
                'titulo': 'PDTIC 2024-2027 - Logística Digital dos Correios',
                'descricao': 'Transformação digital completa dos Correios com implementação de rastreamento em tempo real via IoT, otimização de rotas com IA, digitalização dos processos de importação/exportação e desenvolvimento de serviços de e-commerce integrados.',
                'vigencia_inicio': date(2024, 1, 1),
                'vigencia_fim': date(2027, 12, 31),
                'status': 'elaboracao',
                'versoes': [
                    {'numero_versao': '0.8', 'data_aprovacao': date(2024, 7, 30), 'observacoes': 'Em fase de validação técnica e orçamentária.'},
                ],
            },
            {
                'titulo': 'PDTIC 2025-2029 - Identidade Digital Brasileira',
                'descricao': 'Consolidação da infraestrutura de identidade digital nacional, implementação de carteira digital de documentos, desenvolvimento de soluções de autenticação biométrica avançada e criação de ecossistema de confiança digital para serviços públicos e privados.',
                'vigencia_inicio': date(2025, 1, 1),
                'vigencia_fim': date(2029, 12, 31),
                'status': 'aprovado',
                'versoes': [
                    {'numero_versao': '1.0', 'data_aprovacao': date(2024, 11, 5), 'observacoes': 'Plano aprovado em conformidade com o Marco Legal da Identidade Digital.'},
                ],
            },
        ]

        for i, data in enumerate(pdtic_data):
            # Associar a uma instituição (cíclico)
            instituicao = instituicoes[i % len(instituicoes)]

            pdtic, created = PDTIC.objects.get_or_create(
                titulo=data['titulo'],
                instituicao=instituicao,
                defaults={
                    'descricao': data['descricao'],
                    'vigencia_inicio': data['vigencia_inicio'],
                    'vigencia_fim': data['vigencia_fim'],
                    'status': data['status'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'PDTIC "{pdtic.titulo}" criado para {instituicao.sigla}.'))
            else:
                self.stdout.write(f'PDTIC "{pdtic.titulo}" já existe para {instituicao.sigla}.')

            # Criar versões para o PDTIC
            for versao_data in data['versoes']:
                versao, versao_created = VersaoPDTIC.objects.get_or_create(
                    pdtic=pdtic,
                    numero_versao=versao_data['numero_versao'],
                    defaults={
                        'data_aprovacao': versao_data['data_aprovacao'],
                        'observacoes': versao_data['observacoes'],
                    }
                )
                if versao_created:
                    self.stdout.write(self.style.SUCCESS(f'Versão "{versao.numero_versao}" criada para PDTIC "{pdtic.titulo}".'))
                else:
                    self.stdout.write(f'Versão "{versao.numero_versao}" já existe para PDTIC "{pdtic.titulo}".')

        self.stdout.write(self.style.SUCCESS('População de PDTICs e versões concluída.'))