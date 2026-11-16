from rest_framework import serializers

from .models import (
    Disciplina,
    Horario,
    Recurso,
    Sala,
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

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ["id", "qtd_aluno", "ano", "periodo"]
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