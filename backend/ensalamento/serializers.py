from rest_framework import serializers

from .models import Recurso, Sala

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
