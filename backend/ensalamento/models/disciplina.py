from django.db import models


class Disciplina(models.Model):
    nome = models.CharField(max_length=150)

    class Meta:
        db_table = "disciplina"

    def __str__(self):
        return self.nome
