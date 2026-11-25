from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from contas.models import Usuario


class Professor(models.Model):
    nome = models.CharField(max_length=150)
    matricula = models.IntegerField(unique=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professor",
        limit_choices_to={"tipo": Usuario.TipoUsuario.PROFESSOR},
    )

    class Meta:
        db_table = "professor"

    def clean(self):
        if self.usuario_id and self.usuario.tipo != Usuario.TipoUsuario.PROFESSOR:
            raise ValidationError(
                {"usuario": "O usuário vinculado a um professor deve ter o tipo PROFESSOR."}
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
