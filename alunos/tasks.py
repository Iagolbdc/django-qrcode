from celery import shared_task
from .models import Aluno
from datetime import date
from twilio.rest import Client
import time

@shared_task
def verificar_horarios():
    alunos = Aluno.objects.all()
    print("testando")
    
    for aluno in alunos:
        
        if not aluno.liberado:
            
            if aluno.horario_entrada or aluno.horario_saida:

                horario_entrada = aluno.horario_entrada.time()
                
                if horario_entrada.hour > 8 and not aluno.horario_saida:
                    
                    mensagem = f"Olá! O aluno {aluno.nome} de matricula {aluno.matricula} na data {date.today()} registrou seu horário de entrada em {horario_entrada.strftime( '%H:%M:%S' )} e não registrou seu horário de saída. Por favor, esteja ciente sobre seu horário de entrada e saída."
                    enviar_mensagem.delay(aluno.telefone_responsavel, mensagem)
                    
                    aluno.horario_entrada = None
                    aluno.horario_saida = None
                    aluno.advertencias = aluno.advertencias + 1
                    
                    aluno.save()

                    continue

                if horario_entrada.hour > 8:
                    
                    mensagem = f"Olá! O aluno {aluno.nome} de matricula {aluno.matricula} na data {date.today()} registrou seu horário de entrada em {horario_entrada.strftime( '%H:%M:%S' )}. Por favor, esteja ciente do horário de entrada."
                    enviar_mensagem.delay(aluno.telefone_responsavel, mensagem)
                    
                    aluno.horario_entrada = None
                    aluno.horario_saida = None
                    aluno.advertencias = aluno.advertencias + 1

                    aluno.save()
                    
                    continue

                if not aluno.horario_saida:
                    
                    mensagem = f"Olá! O aluno {aluno.nome} de matricula {aluno.matricula} na data {date.today()} não registrou o horário de saida. Por favor, entre em contato com a coordenação para sabermos o motivo."
                    enviar_mensagem.delay(aluno.telefone_responsavel, mensagem)
                    
                    aluno.horario_saida = None
                    aluno.horario_entrada = None
                    aluno.advertencias = aluno.advertencias + 1

                    aluno.save()
                    
                    continue

            else:
                
                mensagem = f"Olá! O aluno {aluno.nome} de matricula {aluno.matricula} na data {date.today()} não teve seu horário de entrada e de saída registrados. Por favor, entre em contato com a direção."
                enviar_mensagem.delay(aluno.telefone_responsavel, mensagem)
                
                aluno.advertencias = aluno.advertencias + 1

                aluno.save()
        time.sleep(3)
                

@shared_task
def enviar_mensagem(numero, mensagem):
    print("testando")
    account_sid = 'MY_SID'
    auth_token = 'MY_AUTH_TOKEN'
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

#ENVIANDO COM TWILIO

# @shared_task
# def enviar_mensagem(numero, mensagem):
#     print("testando")
#     account_sid = 'AC1b3b2331efb73b7dfb2d40c18112521c'
#     auth_token = '98b673615783b9e8887eb705d4dc5fb9'
#     from_whatsapp_number = 'whatsapp:+14155238886'

#     client = Client(account_sid, auth_token)
#     try:
#         message = client.messages.create(
#                              from_=from_whatsapp_number,
#                              body=mensagem,
#                              to=f"whatsapp:{numero}")
#         print(f'Mensagem enviada para {numero}: {mensagem}, {message.sid}')
#     except Exception as e:
#         print(f'Erro ao enviar mensagem para {numero}: {e}')
