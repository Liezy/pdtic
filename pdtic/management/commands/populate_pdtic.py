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

        # Dados de exemplo para PDTICs
        pdtic_data = [
            {
                'titulo': 'Plano Diretor de Tecnologia da Informação e Comunicação 2024-2028',
                'descricao': 'Plano estratégico para modernização da infraestrutura de TI.',
                'vigencia_inicio': date(2024, 1, 1),
                'vigencia_fim': date(2028, 12, 31),
                'status': 'aprovado',
                'versoes': [
                    {'numero_versao': 'v1.0', 'data_aprovacao': date(2023, 12, 15), 'observacoes': 'Versão inicial aprovada.'},
                    {'numero_versao': 'v1.1', 'data_aprovacao': date(2024, 3, 10), 'observacoes': 'Atualização com correções menores.'},
                ],
            },
            {
                'titulo': 'PDTIC de Inovação e Pesquisa 2025-2030',
                'descricao': 'Foco em inovação tecnológica e pesquisa aplicada.',
                'vigencia_inicio': date(2025, 1, 1),
                'vigencia_fim': date(2030, 12, 31),
                'status': 'elaboracao',
                'versoes': [
                    {'numero_versao': 'v1.0', 'data_aprovacao': date(2024, 11, 20), 'observacoes': 'Primeira versão em elaboração.'},
                ],
            },
            {
                'titulo': 'Plano de TI Sustentável 2023-2027',
                'descricao': 'Estratégia para adoção de práticas sustentáveis em TI.',
                'vigencia_inicio': date(2023, 1, 1),
                'vigencia_fim': date(2027, 12, 31),
                'status': 'publicado',
                'versoes': [
                    {'numero_versao': 'v1.0', 'data_aprovacao': date(2022, 12, 1), 'observacoes': 'Versão publicada.'},
                    {'numero_versao': 'v2.0', 'data_aprovacao': date(2024, 6, 15), 'observacoes': 'Revisão completa com novos objetivos.'},
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