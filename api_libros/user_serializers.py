from rest_framework import serializers
from .modelos.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Crear el usuario usando el método create_user para asegurar el hash de la contraseña
        return Usuario.objects.create_user(**validated_data)