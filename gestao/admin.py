from django.contrib import admin
from .models import (
    Perfil, Comodo, Tarefa, HistoricoExecucao,
    ComodoTemplate, TarefaTemplate
)

admin.site.register(Perfil)
admin.site.register(Comodo)
admin.site.register(Tarefa)
admin.site.register(HistoricoExecucao)
admin.site.register(ComodoTemplate)
admin.site.register(TarefaTemplate)