from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from contas.models import Usuario
from .models import Recurso, Sala


class RecursoCrudTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = Usuario.objects.create_user(
            email="admin@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.ADMINISTRADOR,
        )

        self.professor = Usuario.objects.create_user(
            email="professor@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        self.recurso = Recurso.objects.create(nome="Projetor")

    def test_professor_pode_listar_recursos(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.get("/api/ensalamento/recursos/")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

    def test_administrador_pode_criar_recurso(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/recursos/",
            {"nome": "Laboratório"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Recurso.objects.filter(nome="Laboratório").exists()
        )

    def test_professor_nao_pode_criar_recurso(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.post(
            "/api/ensalamento/recursos/",
            {"nome": "Quadro digital"},
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_nao_pode_criar_recurso_duplicado(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/recursos/",
            {"nome": "Projetor"},
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_administrador_pode_atualizar_recurso(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.patch(
            f"/api/ensalamento/recursos/{self.recurso.id}/",
            {"nome": "Projetor multimídia"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

    def test_administrador_pode_excluir_recurso(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.delete(
            f"/api/ensalamento/recursos/{self.recurso.id}/",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT,
        )


class SalaCrudTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = Usuario.objects.create_user(
            email="admin-sala@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.ADMINISTRADOR,
        )

        self.professor = Usuario.objects.create_user(
            email="professor-sala@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        self.sala = Sala.objects.create(
            nome="B204",
            capacidade=40,
            tipo="Sala de aula",
        )

    def test_professor_pode_listar_salas(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.get(
            "/api/ensalamento/salas/"
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

    def test_administrador_pode_criar_sala(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/salas/",
            {
                "nome": "Laboratório 1",
                "capacidade": 30,
                "tipo": "Laboratório",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Sala.objects.filter(nome="Laboratório 1").exists()
        )

    def test_professor_nao_pode_criar_sala(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.post(
            "/api/ensalamento/salas/",
            {
                "nome": "Sala proibida",
                "capacidade": 20,
                "tipo": "Sala de aula",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_administrador_pode_atualizar_sala(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.patch(
            f"/api/ensalamento/salas/{self.sala.id}/",
            {"capacidade": 50},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

        self.sala.refresh_from_db()
        self.assertEqual(self.sala.capacidade, 50)

    def test_administrador_pode_excluir_sala(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.delete(
            f"/api/ensalamento/salas/{self.sala.id}/",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Sala.objects.filter(id=self.sala.id).exists()
        )

    def test_nao_pode_criar_sala_com_capacidade_negativa(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/salas/",
            {
                "nome": "Sala inválida",
                "capacidade": -1,
                "tipo": "Sala de aula",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )