
from rest_framework import serializers

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
    SolicitacaoTroca,
    Turma,
)


# ============================================================
# RECURSOS
# ============================================================

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = ["id", "nome"]
        read_only_fields = ["id"]

    def validate_nome(self, value):
        nome = value.strip()

        if not nome:
            raise serializers.ValidationError(
                "O nome do recurso não pode ficar vazio."
            )

        return nome


# ============================================================
# SALAS
# ============================================================

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ["id", "nome", "capacidade", "tipo"]
        read_only_fields = ["id"]

    def validate_nome(self, value):
        nome = value.strip()

        if not nome:
            raise serializers.ValidationError(
                "O nome da sala não pode ficar vazio."
            )

        return nome

    def validate_tipo(self, value):
        tipo = value.strip()

        if not tipo:
            raise serializers.ValidationError(
                "O tipo da sala não pode ficar vazio."
            )

        return tipo

    def validate_capacidade(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "A capacidade da sala deve ser maior que zero."
            )

        return value


# ============================================================
# DISCIPLINAS
# ============================================================

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = ["id", "nome"]
        read_only_fields = ["id"]

    def validate_nome(self, value):
        nome = value.strip()

        if not nome:
            raise serializers.ValidationError(
                "O nome da disciplina não pode ficar vazio."
            )

        return nome


# ============================================================
# SEMESTRES
# ============================================================

class SemestreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semestre
        fields = [
            "id",
            "ano",
            "periodo",
            "data_inicio",
            "data_fim",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        data_inicio = attrs.get(
            "data_inicio",
            getattr(self.instance, "data_inicio", None),
        )

        data_fim = attrs.get(
            "data_fim",
            getattr(self.instance, "data_fim", None),
        )

        if data_inicio and data_fim and data_fim <= data_inicio:
            raise serializers.ValidationError({
                "data_fim": (
                    "A data final deve ser posterior à data inicial."
                )
            })

        return attrs


# ============================================================
# TURMAS
# ============================================================

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ["id", "qtd_aluno", "semestre"]
        read_only_fields = ["id"]

    def validate_qtd_aluno(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "A quantidade de alunos deve ser maior que zero."
            )

        return value


# ============================================================
# HORÁRIOS
# ============================================================

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = [
            "id",
            "dia",
            "hora_inicio",
            "hora_fim",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        hora_inicio = attrs.get(
            "hora_inicio",
            getattr(self.instance, "hora_inicio", None),
        )

        hora_fim = attrs.get(
            "hora_fim",
            getattr(self.instance, "hora_fim", None),
        )

        if hora_inicio and hora_fim and hora_fim <= hora_inicio:
            raise serializers.ValidationError({
                "hora_fim": (
                    "A hora final deve ser posterior à hora inicial."
                )
            })

        return attrs


# ============================================================
# RELACIONAMENTO: SALA POSSUI RECURSO
# ============================================================

class PossuiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Possui
        fields = ["id", "sala", "recurso"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        sala = attrs.get(
            "sala",
            getattr(self.instance, "sala", None),
        )

        recurso = attrs.get(
            "recurso",
            getattr(self.instance, "recurso", None),
        )

        if sala is None or recurso is None:
            return attrs

        consulta = Possui.objects.filter(
            sala=sala,
            recurso=recurso,
        )

        if self.instance:
            consulta = consulta.exclude(pk=self.instance.pk)

        if consulta.exists():
            raise serializers.ValidationError(
                "Este recurso já está associado a esta sala."
            )

        return attrs


# ============================================================
# RELACIONAMENTO: DISCIPLINA NECESSITA DE RECURSO
# ============================================================

class NecessitaDeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NecessitaDe
        fields = ["id", "disciplina", "recurso"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        disciplina = attrs.get(
            "disciplina",
            getattr(self.instance, "disciplina", None),
        )

        recurso = attrs.get(
            "recurso",
            getattr(self.instance, "recurso", None),
        )

        if disciplina is None or recurso is None:
            return attrs

        consulta = NecessitaDe.objects.filter(
            disciplina=disciplina,
            recurso=recurso,
        )

        if self.instance:
            consulta = consulta.exclude(pk=self.instance.pk)

        if consulta.exists():
            raise serializers.ValidationError(
                "Este recurso já é exigido por esta disciplina."
            )

        return attrs


# ============================================================
# PROFESSORES
# ============================================================

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ["id", "nome", "matricula", "usuario"]
        read_only_fields = ["id"]

    def validate_nome(self, value):
        nome = value.strip()

        if not nome:
            raise serializers.ValidationError(
                "O nome do professor não pode ficar vazio."
            )

        return nome


# ============================================================
# COORDENADORES
# ============================================================

class CoordenadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenador
        fields = ["id", "nome", "usuario"]
        read_only_fields = ["id"]

    def validate_nome(self, value):
        nome = value.strip()

        if not nome:
            raise serializers.ValidationError(
                "O nome do coordenador não pode ficar vazio."
            )

        return nome


# ============================================================
# ALOCAÇÕES
# ============================================================

class AlocacaoSerializer(serializers.ModelSerializer):
    aviso_capacidade = serializers.SerializerMethodField()

    class Meta:
        model = Alocacao
        fields = [
            "id",
            "horario",
            "professor",
            "sala",
            "turma",
            "disciplina",
            "coordenador",
            "aviso_capacidade",
        ]
        read_only_fields = ["id", "aviso_capacidade"]

    def get_aviso_capacidade(self, obj):
        if obj.turma.qtd_aluno > obj.sala.capacidade:
            return (
                "A quantidade de alunos da turma é maior "
                "que a capacidade da sala."
            )

        return None

    def validate(self, attrs):
        horario = attrs.get(
            "horario",
            getattr(self.instance, "horario", None),
        )

        professor = attrs.get(
            "professor",
            getattr(self.instance, "professor", None),
        )

        sala = attrs.get(
            "sala",
            getattr(self.instance, "sala", None),
        )

        turma = attrs.get(
            "turma",
            getattr(self.instance, "turma", None),
        )

        disciplina = attrs.get(
            "disciplina",
            getattr(self.instance, "disciplina", None),
        )

        conflitos = Alocacao.objects.all()

        if self.instance:
            conflitos = conflitos.exclude(
                pk=self.instance.pk
            )

        # ----------------------------------------------------
        # CONFLITO DE SALA
        # ----------------------------------------------------

        if horario and sala:
            conflito_sala = conflitos.filter(
                sala=sala,
                horario__dia=horario.dia,
                horario__hora_inicio__lt=horario.hora_fim,
                horario__hora_fim__gt=horario.hora_inicio,
            ).exists()

            if conflito_sala:
                raise serializers.ValidationError({
                    "erro": "conflito_sala",
                    "detalhe": (
                        "A sala já está ocupada nesse horário."
                    ),
                })

        # ----------------------------------------------------
        # CONFLITO DE PROFESSOR
        # ----------------------------------------------------

        if horario and professor:
            conflito_professor = conflitos.filter(
                professor=professor,
                horario__dia=horario.dia,
                horario__hora_inicio__lt=horario.hora_fim,
                horario__hora_fim__gt=horario.hora_inicio,
            ).exists()

            if conflito_professor:
                raise serializers.ValidationError({
                    "erro": "conflito_professor",
                    "detalhe": (
                        "O professor já possui uma aula nesse horário."
                    ),
                })

        # ----------------------------------------------------
        # CONFLITO DE TURMA
        # ----------------------------------------------------

        if horario and turma:
            conflito_turma = conflitos.filter(
                turma=turma,
                horario__dia=horario.dia,
                horario__hora_inicio__lt=horario.hora_fim,
                horario__hora_fim__gt=horario.hora_inicio,
            ).exists()

            if conflito_turma:
                raise serializers.ValidationError({
                    "erro": "conflito_turma",
                    "detalhe": (
                        "A turma já possui uma aula nesse horário."
                    ),
                })

        # ----------------------------------------------------
        # RECURSOS NECESSÁRIOS PELA DISCIPLINA
        # ----------------------------------------------------

        if sala and disciplina:
            recursos_necessarios = set(
                NecessitaDe.objects.filter(
                    disciplina=disciplina
                ).values_list("recurso_id", flat=True)
            )

            recursos_disponiveis = set(
                Possui.objects.filter(
                    sala=sala
                ).values_list("recurso_id", flat=True)
            )

            recursos_ausentes = recursos_necessarios - recursos_disponiveis

            if recursos_ausentes:
                nomes_recursos = list(
                    Recurso.objects.filter(
                        id__in=recursos_ausentes
                    ).values_list("nome", flat=True)
                )

                raise serializers.ValidationError({
                    "erro": "recursos_insuficientes",
                    "detalhe": (
                        "A sala não possui todos os recursos "
                        "necessários para esta disciplina."
                    ),
                    "recursos_ausentes": nomes_recursos,
                })

        return attrs


# ============================================================
# TROCA DIRETA DE ALOCAÇÃO
# ============================================================

class TrocaAlocacaoSerializer(serializers.Serializer):
    """
    Valida uma alteração direta de sala e/ou horário.

    A alteração efetiva é realizada pela view responsável,
    que também registra o histórico.
    """

    sala = serializers.PrimaryKeyRelatedField(
        queryset=Sala.objects.all(),
        required=False,
    )

    horario = serializers.PrimaryKeyRelatedField(
        queryset=Horario.objects.all(),
        required=False,
    )

    motivo = serializers.CharField(max_length=255)

    def validate_motivo(self, value):
        motivo = value.strip()

        if not motivo:
            raise serializers.ValidationError(
                "O motivo da troca é obrigatório."
            )

        return motivo

    def validate(self, attrs):
        alocacao = self.context.get("alocacao")

        if alocacao is None:
            raise serializers.ValidationError(
                "A alocação não foi informada para validação."
            )

        if "sala" not in attrs and "horario" not in attrs:
            raise serializers.ValidationError(
                "Informe a nova sala e/ou o novo horário."
            )

        nova_sala = attrs.get("sala", alocacao.sala)
        novo_horario = attrs.get("horario", alocacao.horario)

        if (
            nova_sala == alocacao.sala
            and novo_horario == alocacao.horario
        ):
            raise serializers.ValidationError(
                "A troca não altera a sala nem o horário da alocação."
            )

        validador = AlocacaoSerializer(
            instance=alocacao,
            data={
                "sala": nova_sala.pk,
                "horario": novo_horario.pk,
            },
            partial=True,
        )

        validador.is_valid(raise_exception=True)

        return attrs


# ============================================================
# SOLICITAÇÕES DE TROCA
# ============================================================

class SolicitacaoTrocaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitacaoTroca
        fields = [
            "id",
            "motivo",
            "status",
            "tipo_troca",
            "alocacao_origem",
            "alocacao_destino",
            "professor_solicitante",
        ]
        read_only_fields = ["id", "status"]

    def validate_motivo(self, value):
        motivo = value.strip()

        if not motivo:
            raise serializers.ValidationError(
                "O motivo da solicitação é obrigatório."
            )

        return motivo

    def validate(self, attrs):
        origem = attrs.get(
            "alocacao_origem",
            getattr(self.instance, "alocacao_origem", None),
        )

        destino = attrs.get(
            "alocacao_destino",
            getattr(self.instance, "alocacao_destino", None),
        )

        if origem and destino and origem == destino:
            raise serializers.ValidationError(
                "A alocação de origem e destino não podem ser iguais."
            )

        return attrs


# ============================================================
# HISTÓRICO
# ============================================================

class HistoricoSerializer(serializers.ModelSerializer):
    sala = serializers.CharField(
        source="alocacao.sala.nome",
        read_only=True,
    )

    disciplina = serializers.CharField(
        source="alocacao.disciplina.nome",
        read_only=True,
    )

    class Meta:
        model = Historico
        fields = [
            "id",
            "data_alteracao",
            "motivo",
            "alocacao",
            "solicitacao_troca",
            "sala",
            "disciplina",
        ]
        read_only_fields = fields
