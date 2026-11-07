from django.db import models

class Turma(models.Model):
    qtd_aluno = models.PositiveIntegerField()
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()

    class Meta:
        db_table = "turma"
