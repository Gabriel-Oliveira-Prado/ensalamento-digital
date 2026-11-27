from django.urls import path

from .views import CadastroUsuarioView, ListaUsuarioView, DetalheUsuarioView, AtualizarUsuarioView, ExcluirUsuarioView

urlpatterns = [
    path("", CadastroUsuarioView.as_view(), name="cadastro_usuario"),
    path("lista/", ListaUsuarioView.as_view(), name="lista_usuarios"),
    path("<int:pk>/", DetalheUsuarioView.as_view(), name="detalhe_usuario"),
    path("<int:pk>/atualizar/", AtualizarUsuarioView.as_view(), name="atualizar_usuario"),
    path("<int:pk>/excluir/", ExcluirUsuarioView.as_view(), name="excluir_usuario"),
]