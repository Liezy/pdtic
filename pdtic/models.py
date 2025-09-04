from django.db import models
from instituicoes.models import Instituicao

class PDTIC(models.Model):
    
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('elaboracao', 'Em Elaboração'),
        ('aprovado', 'Aprovado'),
        ('publicado', 'Publicado'),
    ]

    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, related_name="planos")
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    vigencia_inicio = models.DateField()
    vigencia_fim = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.instituicao.sigla})"
    
class VersaoPDTIC(models.Model):
    pdtic = models.ForeignKey(PDTIC, on_delete=models.CASCADE, related_name="versoes")
    numero_versao = models.CharField(max_length=20)  # Ex: v1.0, v2.0
    data_aprovacao = models.DateField(blank=True, null=True)
    documento = models.FileField(upload_to="pdtic_docs/", blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pdtic.titulo} - {self.numero_versao}"