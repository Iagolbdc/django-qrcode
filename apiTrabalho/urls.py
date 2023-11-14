from django.contrib import admin
from django.urls import path, include
from alunos.views import AlunoViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("", AlunoViewset, basename="alunos")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("alunos/", include(router.urls)),
    path("aluno/", include("alunos.urls")),
    path("auth/", include("accounts.urls")),
]
