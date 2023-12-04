import qrcode
from django.db import models
from io import BytesIO
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone 

User = get_user_model()

class Aluno(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alunos")
    nome = models.CharField(max_length=200)
    idade = models.IntegerField(default=0)
    matricula = models.CharField(max_length=100, unique=True, null=False)
    foto = models.ImageField(upload_to="foto-aluno")
    advertencias = models.IntegerField(default=0)
    liberado = models.BooleanField(default=False)

    telefone_responsavel = models.CharField(max_length=20)
    
    horario_entrada = models.DateTimeField(blank=True, null=True)
    horario_saida = models.DateTimeField( blank=True, null=True)

    created = models.DateTimeField(default=timezone.now)
    
    qrcode = models.ImageField(upload_to="qrcode", blank=True, editable=False)

    def __str__(self):
        return f"{self.matricula} - {self.nome}"

    class Meta:
        ordering = ["nome"]
    
@receiver(post_save, sender=Aluno)
def criar_qrcode(sender, instance, created, **kwargs):
    if created:
        
        url = f"http://192.168.1.42:8000/aluno/{instance.id}"  

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        filename = f'aluno_{instance.id}_{instance.nome}_qrcode.png'

        instance.qrcode.save(filename, File(buffer), save=True)
