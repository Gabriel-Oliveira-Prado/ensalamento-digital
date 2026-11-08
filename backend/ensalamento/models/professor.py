
from django.conf import settings
from django.db import models


class Professor(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="professor",
    )

    nome = models.CharField(max_length=150)

    class Meta:
        db_table = "professor"

    def __str__(self):
        return self.nome
