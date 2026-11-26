from django.db import models

from .alocacao import Alocacao
from .professor import Professor


class SolicitacaoTroca(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        APROVADA = "APROVADA", "Aprovada"
        RECUSADA = "RECUSADA", "Recusada"

    class TipoTroca(models.TextChoices):
        SALA = "SALA", "Sala"
        HORARIO = "HORARIO", "Horário"
        AMBOS = "AMBOS", "Sala e Horário"

    motivo = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )
    tipo_troca = models.CharField(
        max_length=20,
        choices=TipoTroca.choices,
    )
    alocacao_origem = models.ForeignKey(
        Alocacao,
        on_delete=models.PROTECT,
        related_name="solicitacoes_origem",
    )
    alocacao_destino = models.ForeignKey(
        Alocacao,
        on_delete=models.PROTECT,
        related_name="solicitacoes_destino",
    )
    professor_solicitante = models.ForeignKey(
        Professor,
        on_delete=models.PROTECT,
        related_name="solicitacoes_troca",
    )

    class Meta:
        db_table = "solicitacao_troca"

    def __str__(self):
        return f"Solicitação #{self.id} ({self.status})"
