from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
from datetime import timedelta

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
    ativa = models.BooleanField(default=True) 

    def __str__(self):
        return self.titulo

    # --- AQUI ESTÁ A MÁGICA QUE FALTAVA ---
    @property
    def dias_restantes(self):
        # Se nunca foi feita, faltam 0 dias (é pra hoje)
        if not self.data_ultima_execucao:
            return 0
        
        hoje = timezone.localdate()
        # Converte a data de execução para data local
        ultima = timezone.localdate(self.data_ultima_execucao)
        
        dias_passados = (hoje - ultima).days
        restante = self.intervalo_dias - dias_passados
        
        # Retorna o maior valor entre 0 e o restante (para não dar negativo)
        return max(0, restante)

    @property
    def proxima_data(self):
        if not self.data_ultima_execucao:
            return timezone.localdate()
        
        ultima = timezone.localdate(self.data_ultima_execucao)
        return ultima + timedelta(days=self.intervalo_dias)

class HistoricoExecucao(models.Model):
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='historico')
    data_conclusao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Tarefa '{self.tarefa.titulo}' concluída em {self.data_conclusao.strftime('%d/%m/%Y')}"