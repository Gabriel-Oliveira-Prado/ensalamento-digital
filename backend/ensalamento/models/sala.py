from django.db import models

class Sala(models.Model):
    capacidade = models.PositiveIntegerField()
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

    class Meta:
        db_table = "sala"

    def __str__(self):
        return self.nome
