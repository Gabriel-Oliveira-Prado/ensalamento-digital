from django.db import models

class Coordenador(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    class Meta:
        db_table = "coordenador"

    def __str__(self):
        return self.nome
