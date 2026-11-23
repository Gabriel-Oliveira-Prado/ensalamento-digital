from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated

from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import PodeCadastrarUsuario, PodeVisualizarUsuario


class CadastroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, PodeCadastrarUsuario]


class ListaUsuarioView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, PodeVisualizarUsuario]


class DetalheUsuarioView(generics.RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, PodeVisualizarUsuario]


class AtualizarUsuarioView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, PodeVisualizarUsuario]


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
