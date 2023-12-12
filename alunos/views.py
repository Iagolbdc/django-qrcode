import time
import csv
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
#from rest_framework.pagination import PageNumberPagination

from datetime import datetime, timezone
from django.shortcuts import get_object_or_404
from .models import Aluno
from .serializers import AlunoSerializer, UpdateAlunoSerializer
from .permissions import  AuthorOrReadOnly
from accounts.serializers import CurrentUserAlunoSerializer
from twilio.rest import Client
from datetime import date

# class customPaginator(PageNumberPagination):
#     page_size = 20
#     page_query_param = "page"
#     page_size_query_param = "page_size"


class AlunoViewset(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
#   pagination_class = customPaginator
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = user)
        return super().perform_create(serializer)


class AlunoRetrieveUpdateDeleteView(
        generics.GenericAPIView,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin
    ):

    serializer_class = UpdateAlunoSerializer
    queryset = Aluno.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_alunos_for_current_user(request: Request):
    user = request.user

    serializer = CurrentUserAlunoSerializer(instance=user, context={"request": request})

    return Response(data=serializer.data, status=status.HTTP_200_OK)

class ListAlunosForUser(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get("username") or None

        queryset = Aluno.objects.all()

        if username is not None:
            return Aluno.objects.filter(user__username=username)
        
        return queryset
    
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def registrar_entrada_aluno(request: Request, pk):
    
    aluno = get_object_or_404(Aluno, id=pk)

    aluno.horario_entrada = datetime.now(timezone.utc)
    aluno.save()

    return Response(data={"message": "horario de entrada registrado com sucesso"}, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def registrar_saida_aluno(request: Request, pk):
    
    aluno = get_object_or_404(Aluno, id=pk)

    aluno.horario_saida = datetime.now(timezone.utc)
    aluno.save()

    return Response(data={"message": "horario de saída registrado com sucesso"}, status=status.HTTP_200_OK)
    


@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def liberar_aluno(request: Request, pk):
    
    aluno = get_object_or_404(Aluno, id=pk)

    if not aluno.liberado:
            
        response = {
            "message": "Aluno liberado com sucesso"
        }
            
        aluno.liberado = True
    else:

        response = {
            "message": "Aluno voltara a receber mensagens com sucesso"
        }

        aluno.liberado = False

    aluno.save()

    return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def criar_alunos(request: Request):
        try:
            # Obtenha o arquivo CSV da requisição
            file = request.FILES['file']

            # Abra o arquivo CSV para leitura
            reader = csv.reader(file.read().decode('utf-8').splitlines())

            # Pule a linha de cabeçalho
            next(reader)

            # Crie uma lista de dicionários para armazenar os dados dos alunos
            alunos_data = []

            # Percorra cada linha do CSV
            for row in reader:
                # Crie um dicionário para os dados do aluno
                aluno_data = {}

                # Extraia os dados das colunas esperadas
                for i, column in enumerate(['nome', 'matricula', 'idade', 'foto', 'telefone_responsavel']):
                    if i < len(row):
                        aluno_data[column] = row[i]

                # Adicione o dicionário à lista
                alunos_data.append(aluno_data)

            # Crie os objetos Aluno em massa usando o serializer
            serializer = AlunoSerializer(data=alunos_data, many=True)
            if not serializer.is_valid():
                return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            return Response(data={"status":"Alunos importados com sucesso!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"Erro ao importar alunos": e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["POST"])
@permission_classes([IsAuthenticated])
def verificar_horarios(request: Request):
    alunos = Aluno.objects.all()
    print("testando")
    
    for aluno in alunos:
        time.sleep(3)
        if not aluno.liberado:
            
            if aluno.horario_entrada or aluno.horario_saida:

                horario_entrada = aluno.horario_entrada.time()
                
                if horario_entrada.hour > 8 and not aluno.horario_saida:
                    
                    mensagem = f"Olá! O aluno {aluno.nome} de matricula {aluno.matricula} na data {date.today()} registrou seu horário de entrada em {horario_entrada.strftime( '%H:%M:%S' )} e não registrou seu horário de saída. Por favor, esteja ciente sobre seu horário de entrada e saída."
                    enviar_mensagem(aluno.telefone_responsavel, mensagem)
                    
                    aluno.horario_entrada = None
                    aluno.horario_saida = None
                    aluno.advertencias = aluno.advertencias + 1
                    
                    aluno.save()

                    continue

                if horario_entrada.hour > 8:
                    
                    mensagem = f"Olá! O aluno {aluno.nome} de matricula {aluno.matricula} na data {date.today()} registrou seu horário de entrada em {horario_entrada.strftime( '%H:%M:%S' )}. Por favor, esteja ciente do horário de entrada."
                    enviar_mensagem(aluno.telefone_responsavel, mensagem)
                    
                    aluno.horario_entrada = None
                    aluno.horario_saida = None
                    aluno.advertencias = aluno.advertencias + 1

                    aluno.save()
                    
                    continue

                if not aluno.horario_saida:
                    
                    mensagem = f"Olá! O aluno {aluno.nome} de matricula {aluno.matricula} na data {date.today()} não registrou o horário de saida. Por favor, entre em contato com a coordenação para sabermos o motivo."
                    enviar_mensagem(aluno.telefone_responsavel, mensagem)
                    
                    aluno.horario_saida = None
                    aluno.horario_entrada = None
                    aluno.advertencias = aluno.advertencias + 1

                    aluno.save()
                    
                    continue

            else:
                
                mensagem = f"Olá! O aluno {aluno.nome} de matricula {aluno.matricula} na data {date.today()} não teve seu horário de entrada e de saída registrados. Por favor, entre em contato com a direção."
                enviar_mensagem(aluno.telefone_responsavel, mensagem)
                
                aluno.advertencias = aluno.advertencias + 1

                aluno.save()
            
        aluno.horario_saida = None
        aluno.horario_entrada = None
        aluno.save()
    
    return Response(data={"message": "Deu tudo certo dento"}, status=status.HTTP_200_OK)
                

def enviar_mensagem(numero, mensagem):
    print("testando")
    account_sid = 'AC1b3b2331efb73b7dfb2d40c18112521c'
    auth_token = '24ca9038dcefc466b1a9f9354a0fb634'
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

    

