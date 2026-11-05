from django.db import models

from .alocacao import Alocacao

class Historico(models.Model):
    data_alteracao = models.DateField()
    motivo = models.CharField(max_length=255)
    alocacao = models.ForeignKey(Alocacao, on_delete=models.PROTECT, related_name="historico")

    class Meta:
        db_table = "historico"
