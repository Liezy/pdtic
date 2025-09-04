from django.db import models

class Instituicao(models.Model):
    nome = models.CharField(max_length=255)
    sigla = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome


class UnidadeAdministrativa(models.Model):
    nome = models.CharField(max_length=255)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, related_name='unidades')

    def __str__(self):
        return f"{self.nome} ({self.instituicao.sigla})"
