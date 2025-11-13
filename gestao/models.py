from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# --- MODELOS DE TEMPLATE (PARA ONBOARDING) ---

class ComodoTemplate(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome do Modelo de Cômodo")
    icone = models.CharField(max_length=50, verbose_name="Nome do Arquivo do Ícone")

    def __str__(self):
        return self.nome

class TarefaTemplate(models.Model):
    comodo_template = models.ForeignKey(ComodoTemplate, on_delete=models.CASCADE, related_name='tarefas_template')
    titulo = models.CharField(max_length=200, verbose_name="Título da Tarefa Modelo")
    intervalo_dias_sugerido = models.IntegerField(default=1, verbose_name="Intervalo de Dias Sugerido")

    def __str__(self):
        return f"{self.titulo} (Modelo para {self.comodo_template.nome})"

# --- MODELOS DO USUÁRIO ---

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    pontos = models.IntegerField(default=0)
    nivel = models.IntegerField(default=1)
    streak_atual = models.IntegerField(default=0, verbose_name="Sequência Atual")
    data_ultima_atividade = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.usuario.username

class Comodo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comodos')
    nome = models.CharField(max_length=100)
    icone = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} (de {self.usuario.username})"

class Tarefa(models.Model):
    comodo = models.ForeignKey(Comodo, on_delete=models.CASCADE, related_name='tarefas')
    titulo = models.CharField(max_length=200)
    intervalo_dias = models.IntegerField(default=1) # Diário = 1, Semanal = 7, etc.
    data_ultima_execucao = models.DateTimeField(null=True, blank=True)
    ativa = models.BooleanField(default=True) # Para "soft delete"

    def __str__(self):
        return self.titulo

class HistoricoExecucao(models.Model):
    # Deleta o histórico se a tarefa for deletada
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='historico')
    data_conclusao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Tarefa '{self.tarefa.titulo}' concluída em {self.data_conclusao.strftime('%d/%m/%Y')}"