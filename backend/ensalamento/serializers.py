
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
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


class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurso
        fields = ["id", "nome"]
        read_only_fields = ["id"]

    def validate_nome(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "O nome do recurso não pode ficar vazio."
            )
        return value


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ["id", "nome", "capacidade", "tipo"]
        read_only_fields = ["id"]

    def validate_nome(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "O nome da sala não pode ficar vazio."
            )
        return value

    def validate_tipo(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "O tipo da sala não pode ficar vazio."
            )
        return value

    def validate_capacidade(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "A capacidade deve ser maior que zero."
            )
        return value


class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = ["id", "nome"]
        read_only_fields = ["id"]

    def validate_nome(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "O nome da disciplina não pode ficar vazio."
            )
        return value


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
                "data_fim": "A data final deve ser posterior à inicial."
            })

        return attrs


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


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ["id", "dia", "hora_inicio", "hora_fim"]
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
                "hora_fim": "A hora final deve ser posterior à inicial."
            })

        return attrs


class PossuiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Possui
        fields = ["id", "sala", "recurso"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        sala = attrs.get("sala", getattr(self.instance, "sala", None))
        recurso = attrs.get(
            "recurso",
            getattr(self.instance, "recurso", None),
        )

        if sala is None or recurso is None:
            return attrs

        consulta = Possui.objects.filter(sala=sala, recurso=recurso)

        if self.instance:
            consulta = consulta.exclude(pk=self.instance.pk)

        if consulta.exists():
            raise serializers.ValidationError(
                "Este recurso já está associado a esta sala."
            )

        return attrs


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


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ["id", "nome", "matricula", "usuario"]
        read_only_fields = ["id"]

    def validate_nome(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "O nome do professor não pode ficar vazio."
            )
        return value

    def validate_usuario(self, usuario):
        from contas.models import Usuario

        if usuario.tipo != Usuario.TipoUsuario.PROFESSOR:
            raise serializers.ValidationError(
                "O usuário vinculado deve ter o tipo PROFESSOR."
            )
        return usuario


class CoordenadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordenador
        fields = ["id", "nome", "usuario"]
        read_only_fields = ["id"]

    def validate_nome(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "O nome do coordenador não pode ficar vazio."
            )
        return value

    def validate_usuario(self, usuario):
        from contas.models import Usuario

        if usuario.tipo != Usuario.TipoUsuario.COORDENADOR:
            raise serializers.ValidationError(
                "O usuário vinculado deve ter o tipo COORDENADOR."
            )
        return usuario


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

    @extend_schema_field(serializers.CharField(allow_null=True))
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

        # Alterações de sala/horário devem usar a rota específica,
        # que exige motivo e registra o histórico.
        if self.instance and not self.context.get("permitir_troca", False):
            sala_alterada = (
                "sala" in attrs and sala != self.instance.sala
            )
            horario_alterado = (
                "horario" in attrs and horario != self.instance.horario
            )

            if sala_alterada or horario_alterado:
                raise serializers.ValidationError({
                    "detail": (
                        "Alterações de sala ou horário devem ser feitas "
                        "pela rota /alocacoes/{id}/trocar/."
                    )
                })

        conflitos = Alocacao.objects.all()

        if self.instance:
            conflitos = conflitos.exclude(pk=self.instance.pk)

        if horario and sala:
            conflito = conflitos.filter(
                sala=sala,
                horario__dia=horario.dia,
                horario__hora_inicio__lt=horario.hora_fim,
                horario__hora_fim__gt=horario.hora_inicio,
            ).exists()

            if conflito:
                raise serializers.ValidationError({
                    "erro": "conflito_sala",
                    "detalhe": "A sala já está ocupada nesse horário.",
                })

        if horario and professor:
            conflito = conflitos.filter(
                professor=professor,
                horario__dia=horario.dia,
                horario__hora_inicio__lt=horario.hora_fim,
                horario__hora_fim__gt=horario.hora_inicio,
            ).exists()

            if conflito:
                raise serializers.ValidationError({
                    "erro": "conflito_professor",
                    "detalhe": (
                        "O professor já possui uma aula nesse horário."
                    ),
                })

        if horario and turma:
            conflito = conflitos.filter(
                turma=turma,
                horario__dia=horario.dia,
                horario__hora_inicio__lt=horario.hora_fim,
                horario__hora_fim__gt=horario.hora_inicio,
            ).exists()

            if conflito:
                raise serializers.ValidationError({
                    "erro": "conflito_turma",
                    "detalhe": "A turma já possui uma aula nesse horário.",
                })

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
                nomes = list(
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
                    "recursos_ausentes": nomes,
                })

        return attrs


class TrocaAlocacaoSerializer(serializers.Serializer):
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
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "O motivo da troca é obrigatório."
            )
        return value

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
                "A troca não altera a sala nem o horário."
            )

        validador = AlocacaoSerializer(
            instance=alocacao,
            data={
                "sala": nova_sala.pk,
                "horario": novo_horario.pk,
            },
            partial=True,
            context={"permitir_troca": True},
        )
        validador.is_valid(raise_exception=True)

        return attrs


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

# ============================================================
# PAINEL
# ============================================================

class PainelAulaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    hora_inicio = serializers.CharField()
    hora_fim = serializers.CharField()
    sala = serializers.CharField()
    disciplina = serializers.CharField()
    professor = serializers.CharField()
    turma = serializers.CharField()
    situacao = serializers.ChoiceField(
        choices=[
            "agendada",
            "encerrada",
            "em_andamento",
            "proxima",
        ]
    )


class PainelSerializer(serializers.Serializer):
    data = serializers.DateField()
    atualizado_em = serializers.DateTimeField()
    aulas = PainelAulaSerializer(many=True)