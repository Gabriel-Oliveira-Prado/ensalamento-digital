from django.db import models
from django.db.models import F, Q

class Horario(models.Model):
    dia = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    class Meta:
        db_table = "horario"
        constraints = [models.CheckConstraint(condition=Q(hora_fim__gt=F("hora_inicio")), name="ck_horario_fim_apos_inicio")]
