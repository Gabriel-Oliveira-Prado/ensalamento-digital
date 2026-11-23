from django.db import models


class Professor(models.Model):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=150)
    matricula = models.IntegerField(unique=True)
    senha = models.CharField(max_length=128)

    class Meta:
        db_table = "professor"

    def __str__(self):
        return self.nome
