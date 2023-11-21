from django.contrib import admin
from django.urls import path, include
from alunos.views import AlunoViewset
from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

router.register("", AlunoViewset, basename="alunos")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("alunos/", include(router.urls)),
    path("aluno/", include("alunos.urls")),
    path("auth/", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
