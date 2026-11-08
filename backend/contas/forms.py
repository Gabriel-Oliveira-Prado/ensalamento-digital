from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Usuario


class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ("email", "tipo")


class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = (
            "email",
            "first_name",
            "last_name",
            "tipo",
        )