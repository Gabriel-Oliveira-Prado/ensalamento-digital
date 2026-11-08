from rest_framework.permissions import BasePermission

from .models import Usuario


class PodeCadastrarUsuario(BasePermission):
    message = "Você não tem permissão para cadastrar usuários."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.tipo in [
                Usuario.TipoUsuario.ADMINISTRADOR,
                Usuario.TipoUsuario.COORDENADOR,
            ]
        )