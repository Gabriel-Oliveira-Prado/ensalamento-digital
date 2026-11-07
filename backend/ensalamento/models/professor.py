from django.db import models

class Professor(models.Model):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=150)

    class Meta:
        db_table = "professor"

    def __str__(self):
        return self.nome
