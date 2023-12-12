from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from .models import User

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=80)
    password = serializers.CharField(min_length=8, write_only=True)
 
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("E-mail já utilizado")
        
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)

        return user
    
class CurrentUserAlunoSerializer(serializers.ModelSerializer):
    alunos = serializers.HyperlinkedRelatedField(many=True, view_name="aluno_detail", queryset=User.objects.all())
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "alunos"]