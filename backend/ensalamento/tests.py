from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from contas.models import Usuario
from .models import (
    Alocacao,
    Coordenador,
    Disciplina,
    Historico,
    Horario,
    NecessitaDe,
    Possui,
    Professor,
    Recurso,
    Sala,
    Semestre,
    Turma,
)


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


class SemestreCrudTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = Usuario.objects.create_user(
            email="admin-semestre@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.ADMINISTRADOR,
        )

        self.professor = Usuario.objects.create_user(
            email="professor-semestre@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        self.semestre = Semestre.objects.create(
            ano=2026,
            periodo=2,
            data_inicio="2026-08-01",
            data_fim="2026-12-15",
        )

    def test_professor_pode_listar_semestres(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.get("/api/ensalamento/semestres/")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

    def test_administrador_pode_criar_semestre(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/semestres/",
            {
                "ano": 2027,
                "periodo": 1,
                "data_inicio": "2027-02-01",
                "data_fim": "2027-06-30",
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Semestre.objects.filter(ano=2027, periodo=1).exists())

    def test_nao_pode_criar_semestre_com_data_fim_invalida(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/semestres/",
            {
                "ano": 2027,
                "periodo": 2,
                "data_inicio": "2027-12-01",
                "data_fim": "2027-08-01",
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)


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

        self.semestre = Semestre.objects.create(
            ano=2026,
            periodo=2,
            data_inicio="2026-08-01",
            data_fim="2026-12-15",
        )

        self.turma = Turma.objects.create(
            qtd_aluno=35,
            semestre=self.semestre,
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
                "semestre": self.semestre.id,
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
                semestre=self.semestre,
            ).exists()
        )

    def test_professor_nao_pode_criar_turma(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.post(
            "/api/ensalamento/turmas/",
            {
                "qtd_aluno": 30,
                "semestre": self.semestre.id,
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
                "semestre": self.semestre.id,
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
class RelacionamentoRecursosTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = Usuario.objects.create_user(
            email="admin-relacionamentos@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.ADMINISTRADOR,
        )

        self.professor = Usuario.objects.create_user(
            email="professor-relacionamentos@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        self.sala = Sala.objects.create(
            nome="B204",
            capacidade=40,
            tipo="Sala de aula",
        )

        self.recurso = Recurso.objects.create(
            nome="Projetor"
        )

        self.disciplina = Disciplina.objects.create(
            nome="Banco de Dados"
        )

    def test_administrador_pode_associar_recurso_a_sala(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/possui/",
            {
                "sala": self.sala.id,
                "recurso": self.recurso.id,
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Possui.objects.filter(
                sala=self.sala,
                recurso=self.recurso,
            ).exists()
        )

    def test_professor_nao_pode_associar_recurso_a_sala(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.post(
            "/api/ensalamento/possui/",
            {
                "sala": self.sala.id,
                "recurso": self.recurso.id,
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_nao_pode_duplicar_recurso_na_mesma_sala(self):
        self.client.force_authenticate(user=self.admin)

        Possui.objects.create(
            sala=self.sala,
            recurso=self.recurso,
        )

        resposta = self.client.post(
            "/api/ensalamento/possui/",
            {
                "sala": self.sala.id,
                "recurso": self.recurso.id,
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_administrador_pode_listar_recursos_da_sala(self):
        self.client.force_authenticate(user=self.admin)

        Possui.objects.create(
            sala=self.sala,
            recurso=self.recurso,
        )

        resposta = self.client.get(
            "/api/ensalamento/possui/"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(resposta.data), 1)

    def test_administrador_pode_remover_recurso_da_sala(self):
        self.client.force_authenticate(user=self.admin)

        relacionamento = Possui.objects.create(
            sala=self.sala,
            recurso=self.recurso,
        )

        resposta = self.client.delete(
            f"/api/ensalamento/possui/{relacionamento.id}/"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Possui.objects.filter(
                id=relacionamento.id
            ).exists()
        )

    def test_administrador_pode_associar_recurso_a_disciplina(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/necessita-de/",
            {
                "disciplina": self.disciplina.id,
                "recurso": self.recurso.id,
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            NecessitaDe.objects.filter(
                disciplina=self.disciplina,
                recurso=self.recurso,
            ).exists()
        )

    def test_professor_nao_pode_associar_recurso_a_disciplina(self):
        self.client.force_authenticate(user=self.professor)

        resposta = self.client.post(
            "/api/ensalamento/necessita-de/",
            {
                "disciplina": self.disciplina.id,
                "recurso": self.recurso.id,
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_nao_pode_duplicar_recurso_exigido_por_disciplina(self):
        self.client.force_authenticate(user=self.admin)

        NecessitaDe.objects.create(
            disciplina=self.disciplina,
            recurso=self.recurso,
        )

        resposta = self.client.post(
            "/api/ensalamento/necessita-de/",
            {
                "disciplina": self.disciplina.id,
                "recurso": self.recurso.id,
            },
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_administrador_pode_remover_recurso_da_disciplina(self):
        self.client.force_authenticate(user=self.admin)

        relacionamento = NecessitaDe.objects.create(
            disciplina=self.disciplina,
            recurso=self.recurso,
        )

        resposta = self.client.delete(
            f"/api/ensalamento/necessita-de/{relacionamento.id}/"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            NecessitaDe.objects.filter(
                id=relacionamento.id
            ).exists()
        )
class AlocacaoCrudTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = Usuario.objects.create_user(
            email="admin-alocacao@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.ADMINISTRADOR,
        )

        self.coordenador_usuario = Usuario.objects.create_user(
            email="coordenador-alocacao@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.COORDENADOR,
        )

        self.professor_usuario = Usuario.objects.create_user(
            email="professor-alocacao@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        self.professor = Professor.objects.create(
            nome="Professor Teste",
            matricula=123456,
            usuario=self.professor_usuario,
        )

        self.coordenador = Coordenador.objects.create(
            nome="Coordenador Teste",
            usuario=self.coordenador_usuario,
        )

        self.sala = Sala.objects.create(
            nome="B204",
            capacidade=40,
            tipo="Sala de aula",
        )

        self.semestre = Semestre.objects.create(
            ano=2026,
            periodo=2,
            data_inicio="2026-08-01",
            data_fim="2026-12-15",
        )

        self.turma = Turma.objects.create(
            qtd_aluno=30,
            semestre=self.semestre,
        )

        self.disciplina = Disciplina.objects.create(
            nome="Banco de Dados",
        )

        self.horario = Horario.objects.create(
            dia="2026-11-20",
            hora_inicio="08:00:00",
            hora_fim="10:00:00",
        )

        self.alocacao = Alocacao.objects.create(
            horario=self.horario,
            professor=self.professor,
            sala=self.sala,
            turma=self.turma,
            disciplina=self.disciplina,
            coordenador=self.coordenador,
        )

    def dados_alocacao(self):
        return {
            "horario": self.horario.id,
            "professor": self.professor.id,
            "sala": self.sala.id,
            "turma": self.turma.id,
            "disciplina": self.disciplina.id,
            "coordenador": self.coordenador.id,
        }

    def test_coordenador_pode_listar_alocacoes(self):
        self.client.force_authenticate(
            user=self.coordenador_usuario
        )

        resposta = self.client.get(
            "/api/ensalamento/alocacoes/"
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(resposta.data), 1)

    def test_administrador_pode_criar_alocacao(self):
        novo_horario = Horario.objects.create(
            dia="2026-11-21",
            hora_inicio="08:00:00",
            hora_fim="10:00:00",
        )

        nova_turma = Turma.objects.create(
            qtd_aluno=25,
            semestre=self.semestre,
        )

        self.client.force_authenticate(user=self.admin)

        dados = {
            "horario": novo_horario.id,
            "professor": self.professor.id,
            "sala": self.sala.id,
            "turma": nova_turma.id,
            "disciplina": self.disciplina.id,
            "coordenador": self.coordenador.id,
        }

        resposta = self.client.post(
            "/api/ensalamento/alocacoes/",
            dados,
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_201_CREATED,
        )

    def test_professor_nao_pode_criar_alocacao(self):
        self.client.force_authenticate(
            user=self.professor_usuario
        )

        resposta = self.client.post(
            "/api/ensalamento/alocacoes/",
            self.dados_alocacao(),
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_nao_pode_alocar_sala_em_horario_conflitante(self):
        nova_turma = Turma.objects.create(
            qtd_aluno=20,
            semestre=self.semestre,
        )

        self.client.force_authenticate(user=self.admin)

        dados = self.dados_alocacao()
        dados["turma"] = nova_turma.id

        resposta = self.client.post(
            "/api/ensalamento/alocacoes/",
            dados,
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            resposta.data["erro"][0],
            "conflito_sala",
        )

    def test_nao_pode_alocar_professor_em_horario_conflitante(self):
        nova_sala = Sala.objects.create(
            nome="B205",
            capacidade=40,
            tipo="Sala de aula",
        )

        nova_turma = Turma.objects.create(
            qtd_aluno=20,
            semestre=self.semestre,
        )

        self.client.force_authenticate(user=self.admin)

        dados = self.dados_alocacao()
        dados["sala"] = nova_sala.id
        dados["turma"] = nova_turma.id

        resposta = self.client.post(
            "/api/ensalamento/alocacoes/",
            dados,
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            resposta.data["erro"][0],
            "conflito_professor",
        )

    def test_nao_pode_alocar_turma_em_horario_conflitante(self):
        nova_sala = Sala.objects.create(
            nome="B206",
            capacidade=40,
            tipo="Sala de aula",
        )

        outro_professor_usuario = Usuario.objects.create_user(
            email="outro-professor@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        novo_professor = Professor.objects.create(
            nome="Outro Professor",
            matricula=654321,
            usuario=outro_professor_usuario,
        )

        self.client.force_authenticate(user=self.admin)

        dados = self.dados_alocacao()
        dados["sala"] = nova_sala.id
        dados["professor"] = novo_professor.id

        resposta = self.client.post(
            "/api/ensalamento/alocacoes/",
            dados,
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            resposta.data["erro"][0],
            "conflito_turma",
        )

   
def test_alteracao_de_sala_deve_usar_rota_de_troca(self):
    nova_sala = Sala.objects.create(
        nome="B207",
        capacidade=40,
        tipo="Sala de aula",
    )

    self.client.force_authenticate(user=self.admin)

    resposta = self.client.patch(
        f"/api/ensalamento/alocacoes/{self.alocacao.id}/",
        {"sala": nova_sala.id},
        format="json",
    )

    self.assertEqual(
        resposta.status_code,
        status.HTTP_400_BAD_REQUEST,
    )

    self.alocacao.refresh_from_db()

    self.assertEqual(self.alocacao.sala, self.sala)
    self.assertEqual(Historico.objects.count(), 0)

    resposta_troca = self.client.post(
        f"/api/ensalamento/alocacoes/{self.alocacao.id}/trocar/",
        {
            "sala": nova_sala.id,
            "motivo": "Alteração administrativa de sala",
        },
        format="json",
    )

    self.assertEqual(
        resposta_troca.status_code,
        status.HTTP_200_OK,
    )

    self.alocacao.refresh_from_db()

    self.assertEqual(self.alocacao.sala, nova_sala)
    self.assertEqual(Historico.objects.count(), 1)
    self.assertEqual(
        self.alocacao.historico.first().motivo,
        "Alteração administrativa de sala",
    )

    def test_administrador_pode_excluir_alocacao(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.delete(
            f"/api/ensalamento/alocacoes/{self.alocacao.id}/",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Alocacao.objects.filter(
                id=self.alocacao.id
            ).exists()
        )


class TrocaHistoricoPainelTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = Usuario.objects.create_user(
            email="admin-troca@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.ADMINISTRADOR,
        )
        self.coordenador_usuario = Usuario.objects.create_user(
            email="coord-troca@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.COORDENADOR,
        )
        self.professor_usuario = Usuario.objects.create_user(
            email="prof-troca@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        self.professor = Professor.objects.create(
            nome="Professor Troca",
            matricula=777001,
            usuario=self.professor_usuario,
        )
        self.coordenador = Coordenador.objects.create(
            nome="Coord Troca",
            usuario=self.coordenador_usuario,
        )
        self.sala_a = Sala.objects.create(
            nome="A101", capacidade=40, tipo="Sala de aula"
        )
        self.sala_b = Sala.objects.create(
            nome="A102", capacidade=40, tipo="Sala de aula"
        )
        self.semestre = Semestre.objects.create(
            ano=2026,
            periodo=2,
            data_inicio="2026-08-01",
            data_fim="2026-12-15",
        )
        self.turma = Turma.objects.create(qtd_aluno=30, semestre=self.semestre)
        self.turma_2 = Turma.objects.create(qtd_aluno=30, semestre=self.semestre)
        self.disciplina = Disciplina.objects.create(nome="Redes")
        self.horario = Horario.objects.create(
            dia="2026-11-20", hora_inicio="08:00:00", hora_fim="10:00:00"
        )
        self.horario_livre = Horario.objects.create(
            dia="2026-11-20", hora_inicio="10:00:00", hora_fim="12:00:00"
        )

        self.alocacao = Alocacao.objects.create(
            horario=self.horario,
            professor=self.professor,
            sala=self.sala_a,
            turma=self.turma,
            disciplina=self.disciplina,
            coordenador=self.coordenador,
        )
        self.url = f"/api/ensalamento/alocacoes/{self.alocacao.id}/trocar/"

    def test_troca_de_sala_atualiza_alocacao_e_gera_historico(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            self.url,
            {"sala": self.sala_b.id, "motivo": "Ar-condicionado quebrado"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.alocacao.refresh_from_db()
        self.assertEqual(self.alocacao.sala, self.sala_b)
        self.assertEqual(self.alocacao.horario, self.horario)
        self.assertEqual(self.alocacao.historico.count(), 1)
        self.assertEqual(
            self.alocacao.historico.first().motivo,
            "Ar-condicionado quebrado",
        )

    def test_troca_de_horario(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            self.url,
            {"horario": self.horario_livre.id, "motivo": "Reposição"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.alocacao.refresh_from_db()
        self.assertEqual(self.alocacao.horario, self.horario_livre)

    def test_troca_exige_motivo(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            self.url,
            {"sala": self.sala_b.id, "motivo": "   "},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Historico.objects.count(), 0)

    def test_troca_exige_sala_ou_horario(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            self.url, {"motivo": "Sem alteração"}, format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_troca_sem_mudanca_real_e_rejeitada(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            self.url,
            {"sala": self.sala_a.id, "motivo": "Igual"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Historico.objects.count(), 0)

    def test_troca_com_conflito_de_sala_nao_altera_nem_gera_historico(self):
        outro_prof_user = Usuario.objects.create_user(
            email="outro@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )
        Alocacao.objects.create(
            horario=self.horario_livre,
            professor=Professor.objects.create(
                nome="Outro",
                matricula=777002,
                usuario=outro_prof_user,
            ),
            sala=self.sala_b,
            turma=self.turma_2,
            disciplina=self.disciplina,
            coordenador=self.coordenador,
        )
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            self.url,
            {
                "sala": self.sala_b.id,
                "horario": self.horario_livre.id,
                "motivo": "Teste conflito",
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.alocacao.refresh_from_db()
        self.assertEqual(self.alocacao.sala, self.sala_a)
        self.assertEqual(Historico.objects.count(), 0)

    def test_professor_nao_pode_trocar(self):
        self.client.force_authenticate(user=self.professor_usuario)

        resposta = self.client.post(
            self.url,
            {"sala": self.sala_b.id, "motivo": "Tentativa"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_403_FORBIDDEN)

    def test_troca_de_alocacao_inexistente_retorna_404(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.post(
            "/api/ensalamento/alocacoes/99999/trocar/",
            {"sala": self.sala_b.id, "motivo": "x"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)

    def test_historico_lista_e_filtra_por_alocacao(self):
        self.client.force_authenticate(user=self.admin)
        self.client.post(
            self.url,
            {"sala": self.sala_b.id, "motivo": "Primeira"},
            format="json",
        )

        resposta = self.client.get(
            f"/api/ensalamento/historico/?alocacao={self.alocacao.id}"
        )
        vazia = self.client.get("/api/ensalamento/historico/?alocacao=999")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)
        self.assertEqual(resposta.data[0]["motivo"], "Primeira")
        self.assertEqual(resposta.data[0]["sala"], "A102")
        self.assertEqual(len(vazia.data), 0)

    def test_historico_exige_autenticacao(self):
        resposta = self.client.get("/api/ensalamento/historico/")

        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_painel_e_publico_e_lista_aulas_do_dia(self):
        resposta = self.client.get("/api/ensalamento/painel/?data=2026-11-20")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["data"], "2026-11-20")
        self.assertEqual(len(resposta.data["aulas"]), 1)
        aula = resposta.data["aulas"][0]
        self.assertEqual(aula["sala"], "A101")
        self.assertEqual(aula["hora_inicio"], "08:00")
        self.assertEqual(aula["professor"], "Professor Troca")
        self.assertNotIn("email", aula)

    def test_painel_dia_sem_aulas(self):
        resposta = self.client.get("/api/ensalamento/painel/?data=2030-01-01")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data["aulas"], [])

    def test_painel_data_invalida(self):
        resposta = self.client.get("/api/ensalamento/painel/?data=abc")

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_painel_reflete_troca_de_sala(self):
        self.client.force_authenticate(user=self.admin)
        self.client.post(
            self.url,
            {"sala": self.sala_b.id, "motivo": "Troca"},
            format="json",
        )
        self.client.force_authenticate(user=None)

        resposta = self.client.get("/api/ensalamento/painel/?data=2026-11-20")

        self.assertEqual(resposta.data["aulas"][0]["sala"], "A102")


class PerfilUsuarioValidacaoTests(TestCase):
    def setUp(self):
        self.user_prof = Usuario.objects.create_user(
            email="prof-val@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )
        self.user_coord = Usuario.objects.create_user(
            email="coord-val@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.COORDENADOR,
        )

    def test_professor_rejeita_usuario_nao_professor(self):
        with self.assertRaises(ValidationError):
            Professor.objects.create(
                nome="Coord Como Prof",
                matricula=999001,
                usuario=self.user_coord,
            )

    def test_coordenador_rejeita_usuario_nao_coordenador(self):
        with self.assertRaises(ValidationError):
            Coordenador.objects.create(
                nome="Prof Como Coord",
                usuario=self.user_prof,
            )

class ProfessorCoordenadorCrudTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = Usuario.objects.create_user(
            email="admin-cadastros@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.ADMINISTRADOR,
        )

        self.professor_usuario = Usuario.objects.create_user(
            email="professor-cadastro@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        self.coordenador_usuario = Usuario.objects.create_user(
            email="coordenador-cadastro@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.COORDENADOR,
        )

        self.professor = Professor.objects.create(
            nome="Professor Original",
            matricula=888001,
            usuario=self.professor_usuario,
        )

        self.coordenador = Coordenador.objects.create(
            nome="Coordenador Original",
            usuario=self.coordenador_usuario,
        )

    def test_professor_pode_listar_professores(self):
        self.client.force_authenticate(user=self.professor_usuario)

        resposta = self.client.get("/api/ensalamento/professores/")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

    def test_administrador_pode_criar_professor(self):
        self.client.force_authenticate(user=self.admin)

        novo_usuario = Usuario.objects.create_user(
            email="novo-professor@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.PROFESSOR,
        )

        resposta = self.client.post(
            "/api/ensalamento/professores/",
            {
                "nome": "Novo Professor",
                "matricula": 888002,
                "usuario": novo_usuario.id,
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Professor.objects.filter(matricula=888002).exists()
        )

    def test_professor_nao_pode_criar_professor(self):
        self.client.force_authenticate(user=self.professor_usuario)

        resposta = self.client.post(
            "/api/ensalamento/professores/",
            {},
            format="json",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_administrador_pode_atualizar_professor(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.patch(
            f"/api/ensalamento/professores/{self.professor.id}/",
            {"nome": "Professor Atualizado"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

        self.professor.refresh_from_db()
        self.assertEqual(self.professor.nome, "Professor Atualizado")

    def test_administrador_pode_excluir_professor(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.delete(
            f"/api/ensalamento/professores/{self.professor.id}/",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Professor.objects.filter(id=self.professor.id).exists()
        )

    def test_coordenador_pode_listar_coordenadores(self):
        self.client.force_authenticate(user=self.coordenador_usuario)

        resposta = self.client.get("/api/ensalamento/coordenadores/")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

    def test_administrador_pode_criar_coordenador(self):
        self.client.force_authenticate(user=self.admin)

        novo_usuario = Usuario.objects.create_user(
            email="novo-coordenador@teste.com",
            password="SenhaForte@123456",
            tipo=Usuario.TipoUsuario.COORDENADOR,
        )

        resposta = self.client.post(
            "/api/ensalamento/coordenadores/",
            {
                "nome": "Novo Coordenador",
                "usuario": novo_usuario.id,
            },
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Coordenador.objects.filter(nome="Novo Coordenador").exists()
        )

    def test_administrador_pode_atualizar_coordenador(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.patch(
            f"/api/ensalamento/coordenadores/{self.coordenador.id}/",
            {"nome": "Coordenador Atualizado"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)

        self.coordenador.refresh_from_db()
        self.assertEqual(self.coordenador.nome, "Coordenador Atualizado")

    def test_administrador_pode_excluir_coordenador(self):
        self.client.force_authenticate(user=self.admin)

        resposta = self.client.delete(
            f"/api/ensalamento/coordenadores/{self.coordenador.id}/",
        )

        self.assertEqual(
            resposta.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Coordenador.objects.filter(id=self.coordenador.id).exists()
        )
