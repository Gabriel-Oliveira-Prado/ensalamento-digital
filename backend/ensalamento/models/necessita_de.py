from django.db import models

from .disciplina import Disciplina
from .recurso import Recurso

class NecessitaDe(models.Model):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name="disciplinas_necessitantes")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="recursos_necessarios")

    class Meta:
        db_table = "necessita_de"
        constraints = [models.UniqueConstraint(fields=["recurso", "disciplina"], name="uq_necessita_recurso_disciplina")]
