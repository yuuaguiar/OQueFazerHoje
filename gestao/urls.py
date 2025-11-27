from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rota principal
    path('', views.dashboard_view, name='dashboard'),
    
    # Ações
    path('concluir-tarefa/<int:tarefa_id>/', views.concluir_tarefa, name='concluir_tarefa'),
    
    # Configurações
    path('configuracoes/', views.configuracoes_view, name='configuracoes'),
    path('configuracoes/comodo/adicionar/', views.add_comodo, name='add_comodo'),
    path('configuracoes/comodo/<int:comodo_id>/deletar/', views.delete_comodo, name='delete_comodo'),
    path('configuracoes/tarefa/adicionar/', views.add_tarefa, name='add_tarefa'),
    
    # Autenticação
    path('cadastro/', views.pagina_cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='gestao/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('configuracoes/tarefa/<int:tarefa_id>/antecipar/', views.antecipar_tarefa, name='antecipar_tarefa'),
    path('configuracoes/tarefa/<int:tarefa_id>/toggle/', views.toggle_tarefa_ativa, name='toggle_tarefa'),

    path('configuracoes/tarefa/<int:tarefa_id>/deletar/', views.delete_tarefa, name='delete_tarefa'),
    path('sobre/', views.sobre_view, name='sobre'),
]