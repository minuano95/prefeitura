from django.urls import path
from .views import * 

app_name = 'home'

urlpatterns = [
    path('', home_view, name='home'),
    
    path('chamados/', chamados_view, name='chamados_view'),
    path('chamado/edita_chamado/<int:chamado_id>/', edita_chamado, name='edita_chamado'),
    path('chamado/deleta_chamado/<int:chamado_id>/', deleta_chamado, name='deleta_chamado'),
    path('chamado/concluir_chamado/<int:chamado_id>/', concluir_chamado, name='concluir_chamado'),
    path('chamado/reabrir_chamado/<int:chamado_id>/', reabrir_chamado, name='reabrir_chamado'),
    path('chamados/abrir_chamado/', abrir_chamado, name='abrir_chamado'),
   
    path('funcionarios/', funcionarios_view, name='funcionarios'),
    path('funcionarios/edita_funcionario/<int:funcionario_id>/', edita_funcionario, name="edita_funcionario"),
    path('funcionarios/exclui_funcionario/<int:funcionario_id>/', exclui_funcionario, name="exclui_funcionario"),
    path('funcionarios/adiciona_funcionario/', adiciona_funcionario, name="adiciona_funcionario"),
    path('funcionarios/deleta_chamado_funcionario/<int:chamado_id>/', deleta_chamado_funcionario, name="deleta_chamado_funcionario"),
   
    path('estatisticas/', estatisticas_view, name='estatisticas'),

    path('setores/', setores_view, name='setores'),
    path('setores/adiciona_setor/', adiciona_setor, name='adiciona_setor'),
    path('setores/edita_setor/<int:setor_id>/', edita_setor, name='edita_setor'),
    path('setores/exclui_setor/<int:setor_id>/', exclui_setor, name='exclui_setor'),

    path('login/', login_view, name='login'),
    path("logout/", logout_view, name="logout"),
]
