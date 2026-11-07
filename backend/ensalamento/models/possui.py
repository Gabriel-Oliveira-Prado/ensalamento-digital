from django.db import models

from .recurso import Recurso
from .sala import Sala

class Possui(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="recursos_possuidos")
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name="salas_possuidoras")

    class Meta:
        db_table = "possui"
        constraints = [models.UniqueConstraint(fields=["sala", "recurso"], name="uq_possui_sala_recurso")]
