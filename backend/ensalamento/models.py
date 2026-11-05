from django.db import models
from django.db.models import F, Q


class Recurso(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "recurso"

    def __str__(self):
        return self.nome


class Sala(models.Model):
    capacidade = models.PositiveIntegerField()
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

    class Meta:
        db_table = "sala"

    def __str__(self):
        return self.nome


class Possui(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name="recursos_possuidos")
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name="salas_possuidoras")

    class Meta:
        db_table = "possui"
        constraints = [models.UniqueConstraint(fields=["sala", "recurso"], name="uq_possui_sala_recurso")]


class Disciplina(models.Model):
    nome = models.CharField(max_length=150)
    codigo = models.PositiveIntegerField(unique=True)

    class Meta:
        db_table = "disciplina"

    def __str__(self):
        return self.nome


class NecessitaDe(models.Model):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE, related_name="disciplinas_necessitantes")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="recursos_necessarios")

    class Meta:
        db_table = "necessita_de"
        constraints = [models.UniqueConstraint(fields=["recurso", "disciplina"], name="uq_necessita_recurso_disciplina")]


class Turma(models.Model):
    qtd_aluno = models.PositiveIntegerField()
    ano = models.PositiveIntegerField()
    periodo = models.PositiveIntegerField()

    class Meta:
        db_table = "turma"


class Horario(models.Model):
    dia = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    class Meta:
        db_table = "horario"
        constraints = [models.CheckConstraint(condition=Q(hora_fim__gt=F("hora_inicio")), name="ck_horario_fim_apos_inicio")]


class Professor(models.Model):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=150)

    class Meta:
        db_table = "professor"

    def __str__(self):
        return self.nome


class Coordenador(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)

    class Meta:
        db_table = "coordenador"

    def __str__(self):
        return self.nome


class Alocacao(models.Model):
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT, related_name="alocacoes")
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT, related_name="alocacoes")
    sala = models.ForeignKey(Sala, on_delete=models.PROTECT, related_name="alocacoes")
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT, related_name="alocacoes")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, related_name="alocacoes")
    coordenador = models.ForeignKey(Coordenador, on_delete=models.PROTECT, related_name="alocacoes")

    class Meta:
        db_table = "alocacao"
        constraints = [
            models.UniqueConstraint(fields=["horario", "sala"], name="uq_alocacao_horario_sala"),
            models.UniqueConstraint(fields=["horario", "professor"], name="uq_alocacao_horario_professor"),
            models.UniqueConstraint(fields=["horario", "turma"], name="uq_alocacao_horario_turma"),
        ]


class Historico(models.Model):
    data_alteracao = models.DateField()
    motivo = models.CharField(max_length=255)
    alocacao = models.ForeignKey(Alocacao, on_delete=models.PROTECT, related_name="historico")

    class Meta:
        db_table = "historico"
