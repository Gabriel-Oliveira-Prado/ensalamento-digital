from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from contas.models import Usuario
from .models import Disciplina, Horario, Recurso, Sala, Turma


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
class DisciplinaCrudTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = Usuario.objects.create_user(
            email="admin-disciplina@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.ADMINISTRADOR,
        )

        self.professor = Usuario.objects.create_user(
            email="professor-disciplina@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        self.disciplina = Disciplina.objects.create(
            nome="Banco de Dados"
        )

    def test_professor_pode_listar_disciplinas(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.get(
            "/api/ensalamento/disciplinas/"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(resposta.data), 1)

    def test_administrador_pode_criar_disciplina(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/disciplinas/",
            {"nome": "Engenharia de Software"},
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            Disciplina.objects.filter(
                nome="Engenharia de Software"
            ).exists()
        )

    def test_professor_nao_pode_criar_disciplina(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.post(
            "/api/ensalamento/disciplinas/",
            {"nome": "Nova Disciplina"},
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_administrador_pode_atualizar_disciplina(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.patch(
            f"/api/ensalamento/disciplinas/{self.disciplina.id}/",
            {"nome": "Banco de Dados Avancado"},
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
        )

        self.disciplina.refresh_from_db()
        self.assertEqual(
            self.disciplina.nome,
            "Banco de Dados Avancado",
        )

    def test_administrador_pode_excluir_disciplina(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.delete(
            f"/api/ensalamento/disciplinas/{self.disciplina.id}/",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Disciplina.objects.filter(
                id=self.disciplina.id
            ).exists()
        )

    def test_nao_pode_criar_disciplina_sem_nome(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/disciplinas/",
            {"nome": "   "},
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class TurmaCrudTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = Usuario.objects.create_user(
            email="admin-turma@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.ADMINISTRADOR,
        )

        self.professor = Usuario.objects.create_user(
            email="professor-turma@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        self.turma = Turma.objects.create(
            qtd_aluno=35,
            ano=2026,
            periodo=2,
        )

    def test_professor_pode_listar_turmas(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.get(
            "/api/ensalamento/turmas/"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(resposta.data), 1)

    def test_administrador_pode_criar_turma(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/turmas/",
            {
                "qtd_aluno": 40,
                "ano": 2026,
                "periodo": 1,
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            Turma.objects.filter(
                qtd_aluno=40,
                ano=2026,
                periodo=1,
            ).exists()
        )

    def test_professor_nao_pode_criar_turma(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.post(
            "/api/ensalamento/turmas/",
            {
                "qtd_aluno": 30,
                "ano": 2026,
                "periodo": 1,
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_administrador_pode_atualizar_turma(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.patch(
            f"/api/ensalamento/turmas/{self.turma.id}/",
            {"qtd_aluno": 45},
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
        )

        self.turma.refresh_from_db()
        self.assertEqual(
            self.turma.qtd_aluno,
            45,
        )

    def test_administrador_pode_excluir_turma(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.delete(
            f"/api/ensalamento/turmas/{self.turma.id}/",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Turma.objects.filter(
                id=self.turma.id
            ).exists()
        )

    def test_nao_pode_criar_turma_com_quantidade_negativa(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/turmas/",
            {
                "qtd_aluno": -1,
                "ano": 2026,
                "periodo": 1,
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class HorarioCrudTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = Usuario.objects.create_user(
            email="admin-horario@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.ADMINISTRADOR,
        )

        self.professor = Usuario.objects.create_user(
            email="professor-horario@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        self.horario = Horario.objects.create(
            dia="2026-11-10",
            hora_inicio="08:00:00",
            hora_fim="10:00:00",
        )

    def test_professor_pode_listar_horarios(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.get(
            "/api/ensalamento/horarios/"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(resposta.data), 1)

    def test_administrador_pode_criar_horario(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/horarios/",
            {
                "dia": "2026-11-11",
                "hora_inicio": "10:00:00",
                "hora_fim": "12:00:00",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            Horario.objects.filter(
                dia="2026-11-11",
                hora_inicio="10:00:00",
                hora_fim="12:00:00",
            ).exists()
        )

    def test_professor_nao_pode_criar_horario(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.post(
            "/api/ensalamento/horarios/",
            {
                "dia": "2026-11-12",
                "hora_inicio": "14:00:00",
                "hora_fim": "16:00:00",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_administrador_pode_atualizar_horario(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.patch(
            f"/api/ensalamento/horarios/{self.horario.id}/",
            {"hora_fim": "11:00:00"},
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
        )

        self.horario.refresh_from_db()
        self.assertEqual(
            str(self.horario.hora_fim),
            "11:00:00",
        )

    def test_administrador_pode_excluir_horario(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.delete(
            f"/api/ensalamento/horarios/{self.horario.id}/",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Horario.objects.filter(
                id=self.horario.id
            ).exists()
        )

    def test_nao_pode_criar_horario_invalido(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/horarios/",
            {
                "dia": "2026-11-13",
                "hora_inicio": "14:00:00",
                "hora_fim": "12:00:00",
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
