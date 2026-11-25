from django.db import models
from django.db.models import F, Q


class Semestre(models.Model):
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()
    data_inicio = models.DateField()
    data_fim = models.DateField()

    class Meta:
        db_table = "semestre"
        constraints = [
            models.CheckConstraint(
                condition=Q(data_fim__gt=F("data_inicio")),
                name="ck_semestre_fim_apos_inicio",
            ),
            models.UniqueConstraint(
                fields=["ano", "periodo"],
                name="uq_semestre_ano_periodo",
            ),
        ]

    def __str__(self):
        return f"{self.ano}.{self.periodo}"
