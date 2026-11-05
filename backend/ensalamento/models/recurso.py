from django.db import models

class Recurso(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "recurso"

    def __str__(self):
        return self.nome
