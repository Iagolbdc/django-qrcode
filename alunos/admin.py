from django.contrib import admin

from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['matricula', "telefone_responsavel", 'created']
    list_filter = ['created']