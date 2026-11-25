
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Usuario


class AutenticacaoTestes(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = self.criar_usuario(
            "admin@teste.com",
            Usuario.TipoUsuario.ADMINISTRADOR
        )
        self.coordenador = self.criar_usuario(
            "coordenador@teste.com",
            Usuario.TipoUsuario.COORDENADOR
        )
        self.professor = self.criar_usuario(
            "professor@teste.com",
            Usuario.TipoUsuario.PROFESSOR
        )

    def criar_usuario(self, email, tipo):
        usuario = Usuario(email=email, tipo=tipo)
        usuario.set_password("SenhaForte@123456")
        usuario.save()
        return usuario

    def obter_token(self, email):
        resposta = self.client.post(
            "/api/auth/token/",
            {
                "email": email,
                "password": "SenhaForte@123456"
            },
            format="json"
        )
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        return resposta.data["access"]

    def autenticar(self, usuario):
        token = self.obter_token(usuario.email)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def dados_usuario(self, email, tipo):
        return {
            "email": email,
            "password": "OutraSenhaForte@123456",
            "first_name": "Usuario",
            "last_name": "Teste",
            "tipo": tipo
        }

    def test_login_com_email_e_senha(self):
        resposta = self.client.post(
            "/api/auth/token/",
            {
                "email": self.admin.email,
                "password": "SenhaForte@123456"
            },
            format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertIn("access", resposta.data)
        self.assertIn("refresh", resposta.data)

    def test_login_com_senha_incorreta(self):
        resposta = self.client.post(
            "/api/auth/token/",
            {
                "email": self.admin.email,
                "password": "senha-errada"
            },
            format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_renovacao_do_token(self):
        resposta_login = self.client.post(
            "/api/auth/token/",
            {
                "email": self.admin.email,
                "password": "SenhaForte@123456"
            },
            format="json"
        )

        resposta = self.client.post(
            "/api/auth/token/refresh/",
            {"refresh": resposta_login.data["refresh"]},
            format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertIn("access", resposta.data)

    def test_administrador_pode_cadastrar_coordenador(self):
        self.autenticar(self.admin)

        resposta = self.client.post(
            "/api/usuarios/",
            self.dados_usuario(
                "novo.coordenador@teste.com",
                Usuario.TipoUsuario.COORDENADOR
            ),
            format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

    def test_coordenador_pode_cadastrar_professor(self):
        self.autenticar(self.coordenador)

        resposta = self.client.post(
            "/api/usuarios/",
            self.dados_usuario(
                "novo.professor@teste.com",
                Usuario.TipoUsuario.PROFESSOR
            ),
            format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)

    def test_coordenador_nao_pode_cadastrar_coordenador(self):
        self.autenticar(self.coordenador)

        resposta = self.client.post(
            "/api/usuarios/",
            self.dados_usuario(
                "outro.coordenador@teste.com",
                Usuario.TipoUsuario.COORDENADOR
            ),
            format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_professor_nao_pode_cadastrar_usuario(self):
        self.autenticar(self.professor)

        resposta = self.client.post(
            "/api/usuarios/",
            self.dados_usuario(
                "outro.usuario@teste.com",
                Usuario.TipoUsuario.PROFESSOR
            ),
            format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)

    def test_usuario_sem_token_nao_pode_cadastrar(self):
        resposta = self.client.post(
            "/api/usuarios/",
            self.dados_usuario(
                "sem.token@teste.com",
                Usuario.TipoUsuario.PROFESSOR
            ),
            format="json"
        )

        self.assertIn(resposta.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_listar_usuarios(self):
        self.autenticar(self.admin)
        resposta = self.client.get("/api/usuarios/lista/")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resposta.data), 3)

    def test_detalhar_usuario(self):
        self.autenticar(self.admin)
        resposta = self.client.get(f"/api/usuarios/{self.professor.id}/")
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["email"], self.professor.email)
        self.assertNotIn("password", resposta.data)

    def test_atualizar_usuario_sem_senha(self):
        self.autenticar(self.admin)
        resposta = self.client.patch(
            f"/api/usuarios/{self.professor.id}/atualizar/",
            {"first_name": "NomeAtualizado"},
            format="json"
        )
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.professor.refresh_from_db()
        self.assertEqual(self.professor.first_name, "NomeAtualizado")

    def test_atualizar_usuario_com_nova_senha(self):
        self.autenticar(self.admin)
        resposta = self.client.patch(
            f"/api/usuarios/{self.professor.id}/atualizar/",
            {"password": "NovaSenhaForte@98765"},
            format="json"
        )
        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        # Verifica se o login funciona com a nova senha
        resposta_login = self.client.post(
            "/api/auth/token/",
            {
                "email": self.professor.email,
                "password": "NovaSenhaForte@98765"
            },
            format="json"
        )
        self.assertEqual(resposta_login.status_code, status.HTTP_200_OK)

    def test_excluir_usuario(self):
        self.autenticar(self.admin)
        usuario_temp = self.criar_usuario("temp@teste.com", Usuario.TipoUsuario.PROFESSOR)
        resposta = self.client.delete(f"/api/usuarios/{usuario_temp.id}/excluir/")
        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Usuario.objects.filter(id=usuario_temp.id).exists())

    def test_impedir_auto_exclusao(self):
        self.autenticar(self.admin)
        resposta = self.client.delete(f"/api/usuarios/{self.admin.id}/excluir/")
        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(Usuario.objects.filter(id=self.admin.id).exists())