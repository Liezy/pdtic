from django.core.management.base import BaseCommand
from instituicoes.models import Instituicao, UnidadeAdministrativa

class Command(BaseCommand):
    help = 'Popula o banco de dados com instituições e unidades administrativas de exemplo'

    def handle(self, *args, **options):
        # Dados de exemplo para instituições e suas unidades
        instituicoes_data = [
            {
                'nome': 'Universidade Federal do Rio de Janeiro',
                'sigla': 'UFRJ',
                'cor_tema': '#FF0000',
                'unidades': [
                    'Faculdade de Engenharia',
                    'Instituto de Matemática',
                    'Instituto de Física',
                    'Faculdade de Medicina',
                ],
            },
            {
                'nome': 'Universidade de São Paulo',
                'sigla': 'USP',
                'cor_tema': '#0000FF',
                'unidades': [
                    'Faculdade de Direito',
                    'Instituto de Química',
                    'Escola de Engenharia de São Carlos',
                    'Faculdade de Economia',
                ],
            },
            {
                'nome': 'Universidade Estadual de Campinas',
                'sigla': 'UNICAMP',
                'cor_tema': '#00FF00',
                'unidades': [
                    'Instituto de Computação',
                    'Faculdade de Engenharia Mecânica',
                    'Instituto de Biologia',
                    'Faculdade de Ciências Médicas',
                ],
            },
            {
                'nome': 'Pontifícia Universidade Católica do Rio de Janeiro',
                'sigla': 'PUC-Rio',
                'cor_tema': '#FFFF00',
                'unidades': [
                    'Departamento de Engenharia Elétrica',
                    'Departamento de Matemática',
                    'Faculdade de Direito',
                    'Centro Técnico Científico',
                ],
            },
            {
                'nome': 'Instituto Tecnológico de Aeronáutica',
                'sigla': 'ITA',
                'cor_tema': '#FF00FF',
                'unidades': [
                    'Divisão de Engenharia Aeronáutica',
                    'Divisão de Engenharia Eletrônica',
                    'Divisão de Engenharia Mecânica',
                    'Centro de Pesquisa',
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