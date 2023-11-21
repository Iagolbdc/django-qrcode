import schedule
import time
from alunos.tasks import verificar_horarios

def agendar_tarefa():
    print("testando")
    verificar_horarios()

# Agende a tarefa para todos os dias às 19 horas
schedule.every().day.at("22:13").do(agendar_tarefa)

# Loop principal para verificar as tarefas agendadas
while True:
    schedule.run_pending()
    time.sleep(1)