from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = Usuario
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "tipo",
        ]
        read_only_fields = ["id"]

    def validate_tipo(self, value):
        solicitante = self.context["request"].user

        if solicitante.tipo == Usuario.TipoUsuario.ADMINISTRADOR:
            if value not in [
                Usuario.TipoUsuario.COORDENADOR,
                Usuario.TipoUsuario.PROFESSOR,
            ]:
                raise serializers.ValidationError(
                    "Administrador só pode cadastrar coordenadores e professores."
                )

        elif solicitante.tipo == Usuario.TipoUsuario.COORDENADOR:
            if value != Usuario.TipoUsuario.PROFESSOR:
                raise serializers.ValidationError(
                    "Coordenador só pode cadastrar professores."
                )

        else:
            raise serializers.ValidationError(
                "Você não tem permissão para cadastrar usuários."
            )

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")

        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()

        return usuario