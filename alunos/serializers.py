from rest_framework import serializers
from .models import Aluno

class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(required=True)
    idade = serializers.IntegerField(required=True)
    matricula = serializers.CharField(required=True)
    foto = serializers.ImageField(required=True)

    class Meta:
        model = Aluno
        fields = ["nome", "idade", "matricula", "foto"]
        read_only_fields = ['qrcode']