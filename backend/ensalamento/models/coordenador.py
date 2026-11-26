from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from contas.models import Usuario


class Coordenador(models.Model):
    nome = models.CharField(max_length=150)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="coordenador",
        limit_choices_to={"tipo": Usuario.TipoUsuario.COORDENADOR},
    )

    class Meta:
        db_table = "coordenador"

    def clean(self):
        if self.usuario_id and self.usuario.tipo != Usuario.TipoUsuario.COORDENADOR:
            raise ValidationError(
                {"usuario": "O usuário vinculado a um coordenador deve ter o tipo COORDENADOR."}
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
