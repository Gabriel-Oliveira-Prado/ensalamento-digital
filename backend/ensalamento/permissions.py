from rest_framework.permissions import BasePermission, SAFE_METHODS

from contas.models import Usuario


class PodeConsultarGerenciarRecursos(BasePermission):
    message = "Você não tem permissão para alterar recursos."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.tipo in [
            Usuario.TipoUsuario.ADMINISTRADOR,
            Usuario.TipoUsuario.COORDENADOR,
        ]

class PodeConsultarGerenciarSalas(BasePermission):
    message = "Você não tem permissão para alterar salas."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.tipo in [
            Usuario.TipoUsuario.ADMINISTRADOR,
            Usuario.TipoUsuario.COORDENADOR,
        ]