
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

        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)
