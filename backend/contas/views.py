from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import PodeCadastrarUsuario, PodeVisualizarUsuario


@extend_schema(
    tags=["Usuários"],
    description="Cadastra usuários. Administradores cadastram coordenadores e professores; coordenadores cadastram professores.",
)
class CadastroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, PodeCadastrarUsuario]


@extend_schema(tags=["Usuários"], description="Lista os usuários autorizados.")
class ListaUsuarioView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, PodeVisualizarUsuario]


@extend_schema(tags=["Usuários"], description="Consulta um usuário pelo identificador.")
class DetalheUsuarioView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, PodeVisualizarUsuario]


@extend_schema(tags=["Usuários"], description="Atualiza os dados de um usuário.")
class AtualizarUsuarioView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, PodeVisualizarUsuario]


@extend_schema(
    tags=["Usuários"],
    description="Exclui um usuário. O usuário autenticado não pode excluir a própria conta.",
)
class ExcluirUsuarioView(generics.DestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, PodeVisualizarUsuario]

    def perform_destroy(self, instance):
        if instance == self.request.user:
            raise serializers.ValidationError(
                {"detail": "Você não pode excluir sua própria conta de usuário."}
            )
        instance.delete()
