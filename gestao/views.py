from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import date
from .models import Perfil, Comodo, Tarefa, HistoricoExecucao

# --- Visão Principal ---

@login_required
def dashboard_view(request):
    perfil = request.user.perfil
    hoje = date.today()

    todas_tarefas = Tarefa.objects.filter(comodo__usuario=request.user, ativa=True)
    
    tarefas_hoje = []
    tarefas_concluidas_hoje_ids = set(
        HistoricoExecucao.objects.filter(
            tarefa__in=todas_tarefas,
            data_conclusao__date=hoje
        ).values_list('tarefa_id', flat=True)
    )

    for t in todas_tarefas:
        vencida = True
        if t.data_ultima_execucao:
            dias_passados = (hoje - t.data_ultima_execucao.date()).days
            if dias_passados < t.intervalo_dias:
                vencida = False
        
        is_completed_today = t.id in tarefas_concluidas_hoje_ids

        if vencida or is_completed_today:
            t.is_completed_today = is_completed_today
            tarefas_hoje.append(t)

    tarefas_hoje_count = len(tarefas_hoje)
    tarefas_concluidas_count = len(tarefas_concluidas_hoje_ids)
    all_completed = (tarefas_hoje_count > 0) and (tarefas_concluidas_count == tarefas_hoje_count)
    
    progresso_percentual = 0
    if tarefas_hoje_count > 0:
        progresso_percentual = int((tarefas_concluidas_count / tarefas_hoje_count) * 100)

    context = {
        'perfil': perfil,
        'tarefas_hoje': tarefas_hoje,
        'tarefas_hoje_count': tarefas_hoje_count,
        'tarefas_concluidas_count': tarefas_concluidas_count,
        'all_completed': all_completed,
        'progresso_percentual': progresso_percentual,
        'comodos': comodos,
    }
    return render(request, 'gestao/dashboard.html', context)

@login_required
def concluir_tarefa(request, tarefa_id):
    if request.method == 'POST':
        tarefa = get_object_or_404(Tarefa, id=tarefa_id, comodo__usuario=request.user)
        hoje = timezone.now().date()
        exec_hoje = HistoricoExecucao.objects.filter(tarefa=tarefa, data_conclusao__date=hoje).first()

        if exec_hoje:
            exec_hoje.delete()
        else:
            HistoricoExecucao.objects.create(tarefa=tarefa)
            tarefa.data_ultima_execucao = timezone.now()
            tarefa.save()

    return redirect('dashboard')

# --- Visões de Configuração ---

@login_required
def configuracoes_view(request):
    comodos = Comodo.objects.filter(usuario=request.user)
    context = {
        'comodos': comodos
    }
    return render(request, 'gestao/configuracoes.html', context)

@login_required
def add_comodo(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        icone = request.POST.get('icone', 'default.png')
        if nome:
            Comodo.objects.create(usuario=request.user, nome=nome, icone=icone)
    return redirect('configuracoes')

@login_required
def delete_comodo(request, comodo_id):
    if request.method == 'POST':
        comodo = get_object_or_404(Comodo, id=comodo_id, usuario=request.user)
        comodo.delete()
    return redirect('configuracoes')

@login_required
def add_tarefa(request):
    if request.method == 'POST':
        comodo_id = request.POST.get('comodo_id')
        titulo = request.POST.get('titulo')
        intervalo_dias = request.POST.get('intervalo_dias', 1)
        
        comodo = get_object_or_404(Comodo, id=comodo_id, usuario=request.user)
        if titulo and comodo:
            Tarefa.objects.create(
                comodo=comodo,
                titulo=titulo,
                intervalo_dias=int(intervalo_dias)
            )
    return redirect('configuracoes')

# --- Visões de Autenticação ---

def pagina_cadastro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'gestao/cadastro.html', {'form': form})