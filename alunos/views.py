from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination

from datetime import datetime, timezone
from django.shortcuts import get_object_or_404
from .models import Aluno
from .serializers import AlunoSerializer
from .permissions import  AuthorOrReadOnly
from accounts.serializers import CurrentUserAlunoSerializer

class customPaginator(PageNumberPagination):
    page_size = 20
    page_query_param = "page"
    page_size_query_param = "page_size"


class AlunoViewset(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = customPaginator

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = user)
        return super().perform_create(serializer)


class AlunoRetrieveUpdateDeleteView(
        generics.GenericAPIView,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin
    ):

    serializer_class = AlunoSerializer
    queryset = Aluno.objects.all()
    permission_classes = [AuthorOrReadOnly]

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request: Request, *args, **kwargs):
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
    

