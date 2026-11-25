from django.db import models

from .alocacao import Alocacao
from .solicitacao_troca import SolicitacaoTroca


class Historico(models.Model):
    data_alteracao = models.DateTimeField()
    motivo = models.CharField(max_length=255)
    alocacao = models.ForeignKey(
        Alocacao,
        on_delete=models.PROTECT,
        related_name="historico",
    )
    solicitacao_troca = models.ForeignKey(
        SolicitacaoTroca,
        on_delete=models.PROTECT,
        related_name="historicos",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "historico"
