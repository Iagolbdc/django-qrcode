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
    path("<int:pk>/entrada_aluno/", views.registrar_entrada_aluno, name="registrar_entrada_aluno"),
    path("<int:pk>/saida_aluno/", views.registrar_saida_aluno, name="registrar_saida_aluno"),
    path("<int:pk>/liberar_aluno/", views.liberar_aluno, name="liberar_aluno"),
]