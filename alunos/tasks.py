from celery import shared_task
from django.utils import timezone
from .models import Aluno
from twilio.rest import Client

@shared_task
def verificar_horarios():
    alunos = Aluno.objects.all()
    print("testando")
    for aluno in alunos:
        if aluno.horario_entrada:
            horario_entrada = aluno.horario_entrada.time()
            if horario_entrada.hour > 8:
                mensagem = f"Olá! O aluno {aluno.nome} chegou às {horario_entrada}. Por favor, esteja ciente do horário de entrada."
                enviar_mensagem.delay(aluno.telefone_responsavel, mensagem)
                aluno.horario_entrada = None
        else:
            mensagem = f"Olá! O aluno {aluno.nome} não veio para a escola hoje. Por favor, entre em contato com a direção."
            enviar_mensagem(aluno.telefone_responsavel, mensagem)

@shared_task
def enviar_mensagem(numero, mensagem):
    print("testando")
    account_sid = 'AC1b3b2331efb73b7dfb2d40c18112521c'
    auth_token = '98b673615783b9e8887eb705d4dc5fb9'
    from_whatsapp_number = 'whatsapp:+14155238886'

    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
                             from_=from_whatsapp_number,
                             body=mensagem,
                             to=f"whatsapp:{numero}")
        print(f'Mensagem enviada para {numero}: {mensagem}, {message.sid}')
    except Exception as e:
        print(f'Erro ao enviar mensagem para {numero}: {e}')
