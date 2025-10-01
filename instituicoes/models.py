from django.db import models

class Instituicao(models.Model):
    nome = models.CharField(max_length=255)
    sigla = models.CharField(max_length=20, blank=True, null=True)
    cor_tema = models.CharField(
        max_length=7, 
        default='#3B82F6',
        help_text='Cor tema da instituição em formato hexadecimal (ex: #3B82F6)'
    )

    def __str__(self):
        return self.nome


class UnidadeAdministrativa(models.Model):
    nome = models.CharField(max_length=255)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, related_name='unidades')

    def __str__(self):
        return f"{self.nome} ({self.instituicao.sigla})"
