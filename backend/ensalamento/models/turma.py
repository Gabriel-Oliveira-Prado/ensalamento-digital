from django.db import models

from .semestre import Semestre


class Turma(models.Model):
    qtd_aluno = models.PositiveIntegerField()
    semestre = models.ForeignKey(
        Semestre,
        on_delete=models.PROTECT,
        related_name="turmas",
    )

    class Meta:
        db_table = "turma"

    def __str__(self):
        return f"Turma {self.id} ({self.semestre})"
