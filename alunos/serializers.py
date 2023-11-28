from rest_framework.validators import ValidationError
from rest_framework import serializers
from .models import Aluno

class AlunoSerializer(serializers.ModelSerializer):
    matricula = serializers.CharField(required=False)

    class Meta:
        model = Aluno
        fields = ["id" ,"nome", 'qrcode',"idade", "matricula", "foto", "telefone_responsavel", "horario_entrada", "horario_saida", "advertencias", "liberado"]
        read_only_fields = ["id",'qrcode', "horario_entrada", "horario_saida", "advertencias", "liberado"]

    def validate(self, attrs):
        matricula_exists = Aluno.objects.filter(matricula=attrs["matricula"]).exists()

        if matricula_exists:
            raise ValidationError("Matricula já foi utilizada")
        
        return super().validate(attrs)

