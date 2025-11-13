from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil, Comodo, Tarefa, HistoricoExecucao, ComodoTemplate
from datetime import date, timedelta

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # 1. Cria o perfil
        Perfil.objects.create(usuario=instance)
        
        # 2. Onboarding Automático: Clona todos os templates para o usuário
        comodo_templates = ComodoTemplate.objects.all()
        for ct in comodo_templates:
            novo_comodo = Comodo.objects.create(
                usuario=instance,
                nome=ct.nome,
                icone=ct.icone
            )
            for tt in ct.tarefas_template.all():
                Tarefa.objects.create(
                    comodo=novo_comodo,
                    titulo=tt.titulo,
                    intervalo_dias=tt.intervalo_dias_sugerido
                )

@receiver(post_save, sender=HistoricoExecucao)
def premiar_usuario_por_tarefa(sender, instance, created, **kwargs):
    if not created:
        return 

    perfil = instance.tarefa.comodo.usuario.perfil
    tarefa_especifica = instance.tarefa
    hoje = date.today()

    # --- LÓGICA DE PONTOS (Uma vez POR TAREFA, por dia) ---
    conclusoes_desta_tarefa_hoje = HistoricoExecucao.objects.filter(
        tarefa=tarefa_especifica,
        data_conclusao__date=hoje
    ).count()

    pontos_ganhos = 0
    if conclusoes_desta_tarefa_hoje == 1:
        pontos_ganhos = 10 
        perfil.pontos += pontos_ganhos

    # --- LÓGICA DE STREAK (Uma vez POR USUÁRIO, por dia) ---
    if perfil.data_ultima_atividade != hoje:
        ontem = hoje - timedelta(days=1)
        if perfil.data_ultima_atividade == ontem:
            perfil.streak_atual += 1
        else:
            perfil.streak_atual = 1
        
        perfil.data_ultima_atividade = hoje
    
    # --- LÓGICA DE SUBIR DE NÍVEL ---
    if pontos_ganhos > 0:
        if perfil.pontos >= perfil.nivel * 100:
            perfil.nivel += 1
    
    perfil.save()