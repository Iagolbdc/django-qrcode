from . import views
from django.urls import path

urlpatterns = [
    path(
        "<int:pk>",
        views.AlunoRetrieveUpdateDeleteView.as_view(),
        name="aluno_detail",
    ),
    path("current_user/", views.get_alunos_for_current_user, name="current_user"),
    path("alunos_for/", views.ListAlunosForUser.as_view(), name="alunos_for_current_user"),
    path("entrada_aluno/<int:pk>/", views.registrar_entrada_aluno, name="registrar_entrada_aluno"),
    path("saida_aluno/<int:pk>/", views.registrar_saida_aluno, name="registrar_saida_aluno")
,]