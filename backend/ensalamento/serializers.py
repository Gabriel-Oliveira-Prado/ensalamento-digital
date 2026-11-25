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

class SemestreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semestre
        fields = ["id", "ano", "periodo", "data_inicio", "data_fim"]
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
            raise serializers.ValidationError(
                "A data final deve ser posterior à data inicial."
            )

        return attrs


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ["id", "qtd_aluno", "semestre"]
        read_only_fields = ["id"]


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
            raise serializers.ValidationError(
                "A hora final deve ser posterior à hora inicial."
            )

        return attrs

class PossuiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Possui
        fields = ["id", "sala", "recurso"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        sala = attrs["sala"]
        recurso = attrs["recurso"]

        if Possui.objects.filter(
            sala=sala,
            recurso=recurso,
        ).exists():
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
        disciplina = attrs["disciplina"]
        recurso = attrs["recurso"]

        if NecessitaDe.objects.filter(
            disciplina=disciplina,
            recurso=recurso,
        ).exists():
            raise serializers.ValidationError(
                "Este recurso já é exigido por esta disciplina."
            )

        return attrs

class AlocacaoSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = ["id"]

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

        conflitos = Alocacao.objects.all()

        if self.instance:
            conflitos = conflitos.exclude(
                id=self.instance.id
            )

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
                    "detalhe": "A sala já está ocupada nesse horário.",
                })

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
                    "detalhe": "O professor já possui uma aula nesse horário.",
                })

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
                    "detalhe": "A turma já possui uma aula nesse horário.",
                })

        return attrs


class TrocaAlocacaoSerializer(serializers.Serializer):
    """Valida o pedido de troca de sala e/ou horário de uma alocação."""

    sala = serializers.PrimaryKeyRelatedField(
        queryset=Sala.objects.all(), required=False
    )
    horario = serializers.PrimaryKeyRelatedField(
        queryset=Horario.objects.all(), required=False
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
        alocacao = self.context["alocacao"]

        if "sala" not in attrs and "horario" not in attrs:
            raise serializers.ValidationError(
                "Informe a nova sala e/ou o novo horário."
            )

        nova_sala = attrs.get("sala", alocacao.sala)
        novo_horario = attrs.get("horario", alocacao.horario)

        if nova_sala == alocacao.sala and novo_horario == alocacao.horario:
            raise serializers.ValidationError(
                "A troca não altera a sala nem o horário da alocação."
            )

        # Reaproveita as regras de conflito de sala, professor e turma.
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


class HistoricoSerializer(serializers.ModelSerializer):
    sala = serializers.CharField(source="alocacao.sala.nome", read_only=True)
    disciplina = serializers.CharField(
        source="alocacao.disciplina.nome", read_only=True
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