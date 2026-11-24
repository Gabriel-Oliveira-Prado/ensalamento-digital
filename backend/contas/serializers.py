from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        validators=[validate_password]
    )

    class Meta:
        model = Usuario
        fields = ["id", "email", "password", "first_name", "last_name", "tipo"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        request = self.context.get("request")

        # Na criação, a senha é obrigatória
        if not self.instance and not attrs.get("password"):
            raise serializers.ValidationError({"password": "A senha é obrigatória."})

        # Validação de hierarquia de permissões para tipo
        if "tipo" in attrs and request and request.user.is_authenticated:
            solicitante = request.user
            tipo = attrs["tipo"]

            if solicitante.tipo == Usuario.TipoUsuario.ADMINISTRADOR:
                if tipo not in [Usuario.TipoUsuario.COORDENADOR, Usuario.TipoUsuario.PROFESSOR]:
                    raise serializers.ValidationError(
                        {"tipo": "Administrador só pode cadastrar coordenadores e professores."}
                    )
            elif solicitante.tipo == Usuario.TipoUsuario.COORDENADOR:
                if tipo != Usuario.TipoUsuario.PROFESSOR:
                    raise serializers.ValidationError(
                        {"tipo": "Coordenador só pode cadastrar professores."}
                    )

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance