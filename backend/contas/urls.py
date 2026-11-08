from django.urls import path

from .views import CadastroUsuarioView

urlpatterns = [
    path("", CadastroUsuarioView.as_view(), name="cadastro_usuario"),
]