
from rest_framework.permissions import BasePermission, SAFE_METHODS

from contas.models import Usuario


class PermissaoBaseEnsalamento(BasePermission):
    message = "Você não tem permissão para realizar esta operação."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.tipo in (
            Usuario.TipoUsuario.ADMINISTRADOR,
            Usuario.TipoUsuario.COORDENADOR,
        )


class PodeConsultarGerenciarRecursos(PermissaoBaseEnsalamento):
    message = "Você não tem permissão para alterar recursos."


class PodeConsultarGerenciarSalas(PermissaoBaseEnsalamento):
    message = "Você não tem permissão para alterar salas."


class PodeConsultarGerenciarCadastros(PermissaoBaseEnsalamento):
    message = "Você não tem permissão para alterar este cadastro."
