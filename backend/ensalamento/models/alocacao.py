from django.db import models

from .coordenador import Coordenador
from .disciplina import Disciplina
from .horario import Horario
from .professor import Professor
from .sala import Sala
from .turma import Turma


class Alocacao(models.Model):
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT)
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT)
    sala = models.ForeignKey(Sala, on_delete=models.PROTECT)
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT)
    coordenador = models.ForeignKey(Coordenador, on_delete=models.PROTECT)

    class Meta:
        db_table = "alocacao"
