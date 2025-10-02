from django.core.management.base import BaseCommand
from instituicoes.models import Instituicao, UnidadeAdministrativa

class Command(BaseCommand):
    help = 'Popula o banco de dados com instituições e unidades administrativas de exemplo'

    def handle(self, *args, **options):
        # Dados reais de instituições públicas brasileiras e suas unidades administrativas
        instituicoes_data = [
            {
                'nome': 'Ministério da Fazenda',
                'sigla': 'MF',
                'cor_tema': '#1E3A8A',  # Azul institucional
                'unidades': [
                    'Secretaria Executiva',
                    'Secretaria do Tesouro Nacional',
                    'Receita Federal do Brasil',
                    'Secretaria de Política Econômica',
                    'Procuradoria-Geral da Fazenda Nacional',
                    'Conselho Administrativo de Recursos Fiscais',
                    'Escola de Administração Fazendária',
                    'Secretaria de Avaliação, Planejamento, Energia e Loteria',
                ],
            },
            {
                'nome': 'Tribunal de Contas da União',
                'sigla': 'TCU',
                'cor_tema': '#059669',  # Verde institucional
                'unidades': [
                    'Presidência',
                    'Secretaria-Geral de Controle Externo',
                    'Secretaria-Geral da Presidência',
                    'Secretaria-Geral de Administração',
                    'Instituto Serzedello Corrêa',
                    'Secretaria de Controle Externo da Administração do Estado',
                    'Secretaria de Controle Externo de Aquisições Logísticas',
                    'Secretaria de Tecnologia da Informação',
                ],
            },
            {
                'nome': 'Banco Central do Brasil',
                'sigla': 'BACEN',
                'cor_tema': '#DC2626',  # Vermelho institucional
                'unidades': [
                    'Diretoria Colegiada',
                    'Departamento de Tecnologia da Informação',
                    'Departamento de Operações Bancárias e de Sistema de Pagamentos',
                    'Departamento de Organização do Sistema Financeiro',
                    'Departamento de Regulação do Sistema Financeiro',
                    'Departamento de Supervisão de Conduta',
                    'Departamento de Relacionamento com Investidores e Estudos Especiais',
                    'Departamento de Assuntos Internacionais',
                ],
            },
            {
                'nome': 'Instituto Nacional do Seguro Social',
                'sigla': 'INSS',
                'cor_tema': '#7C3AED',  # Roxo institucional
                'unidades': [
                    'Presidência',
                    'Diretoria de Benefícios',
                    'Diretoria de Atendimento',
                    'Diretoria de Tecnologia da Informação',
                    'Procuradoria Federal Especializada',
                    'Auditoria Interna',
                    'Corregedoria-Geral',
                    'Superintendências Regionais',
                ],
            },
            {
                'nome': 'Controladoria-Geral da União',
                'sigla': 'CGU',
                'cor_tema': '#B45309',  # Laranja institucional
                'unidades': [
                    'Ministro de Estado',
                    'Secretaria de Combate à Corrupção',
                    'Secretaria Federal de Controle Interno',
                    'Secretaria de Transparência e Prevenção da Corrupção',
                    'Ouvidoria-Geral da União',
                    'Corregedoria-Geral da União',
                    'Controladoria Regional da União no Distrito Federal',
                    'Coordenação-Geral de Recursos Logísticos',
                ],
            },
            {
                'nome': 'Agência Nacional de Telecomunicações',
                'sigla': 'ANATEL',
                'cor_tema': '#0891B2',  # Ciano institucional
                'unidades': [
                    'Conselho Diretor',
                    'Superintendência de Competição',
                    'Superintendência de Controle de Obrigações',
                    'Superintendência de Outorga e Recursos à Prestação',
                    'Superintendência de Fiscalização',
                    'Superintendência de Planejamento e Regulamentação',
                    'Superintendência de Gestão Interna',
                    'Procuradoria Federal Especializada',
                ],
            },
            {
                'nome': 'Empresa Brasileira de Correios e Telégrafos',
                'sigla': 'ECT',
                'cor_tema': '#FACC15',  # Amarelo dos Correios
                'unidades': [
                    'Presidência',
                    'Diretoria Regional São Paulo Metropolitana',
                    'Diretoria Regional Rio de Janeiro',
                    'Diretoria Regional Brasília',
                    'Diretoria de Tecnologia e Inovação',
                    'Diretoria de Gestão de Pessoas',
                    'Diretoria de Administração e Finanças',
                    'Diretoria de Negócios',
                ],
            },
            {
                'nome': 'Instituto Nacional de Tecnologia da Informação',
                'sigla': 'ITI',
                'cor_tema': '#6366F1',  # Índigo tecnológico
                'unidades': [
                    'Presidência',
                    'Diretoria de Políticas e Tecnologias da Informação',
                    'Diretoria de Infraestrutura de Chaves Públicas',
                    'Coordenação-Geral de Certificação Digital',
                    'Coordenação-Geral de Segurança Cibernética',
                    'Coordenação-Geral de Identidade Digital',
                    'Assessoria de Gestão Estratégica',
                    'Centro de Pesquisa e Desenvolvimento',
                ],
            },
        ]

        for data in instituicoes_data:
            instituicao, created = Instituicao.objects.get_or_create(
                nome=data['nome'],
                defaults={
                    'sigla': data['sigla'],
                    'cor_tema': data['cor_tema'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Instituição "{instituicao.nome}" criada com sucesso.'))
            else:
                self.stdout.write(f'Instituição "{instituicao.nome}" já existe.')

            # Criar unidades para a instituição
            for unidade_nome in data['unidades']:
                unidade, unidade_created = UnidadeAdministrativa.objects.get_or_create(
                    nome=unidade_nome,
                    instituicao=instituicao
                )
                if unidade_created:
                    self.stdout.write(self.style.SUCCESS(f'Unidade "{unidade.nome}" criada para {instituicao.sigla}.'))
                else:
                    self.stdout.write(f'Unidade "{unidade.nome}" já existe para {instituicao.sigla}.')

        self.stdout.write(self.style.SUCCESS('População de instituições e unidades concluída.'))