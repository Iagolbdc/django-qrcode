from rest_framework.validators import ValidationError
from rest_framework import serializers
from .models import Aluno

class AlunoSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(required=True)
    idade = serializers.IntegerField(required=True)
    matricula = serializers.CharField(required=True)
    foto = serializers.ImageField(required=True)
    telefone_responsavel = serializers.CharField(max_length=20)

    class Meta:
        model = Aluno
        fields = ["id" ,"nome", 'qrcode',"idade", "matricula", "foto", "telefone_responsavel", "horario_entrada", "horario_saida"]
        read_only_fields = ["id",'qrcode', "horario_entrada", "horario_saida"]

    def validate(self, attrs):
        matricula_exists = Aluno.objects.filter(matricula=attrs["matricula"]).exists()

        if matricula_exists:
            raise ValidationError("Matricula já foi utilizada")
        
        return super().validate(attrs)

