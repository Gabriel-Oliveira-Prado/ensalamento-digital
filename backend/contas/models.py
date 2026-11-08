
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa de um e-mail.")

        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("tipo", "ADMINISTRADOR")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário precisa ter is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário precisa ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):

    class TipoUsuario(models.TextChoices):
        PROFESSOR = "PROFESSOR", "Professor"
        COORDENADOR = "COORDENADOR", "Coordenador"
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"

    username = None

    email = models.EmailField(unique=True)

    tipo = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
    )

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
