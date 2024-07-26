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
    path('chamados/abrir_chamado/', home_view, name='abrir_chamado'),
   
    path('funcionarios/', funcionarios_view, name='funcionarios'),
    path('funcionarios/edita_funcionario/<int:funcionario_id>/', edita_funcionario, name="edita_funcionario"),
    path('funcionarios/exclui_funcionario/<int:funcionario_id>/', exclui_funcionario, name="exclui_funcionario"),
    # path('funcionarios/adiciona_funcionario/', adiciona_funcionario, name="adiciona_funcionario"),
    # path('funcionarios/deleta_agendamento_funcionario/<int:agendamento_id>/', deleta_agendamento_funcionario, name="deleta_agendamento_funcionario"),
   
    path('login/', login_view, name='login'),
    path("logout/", logout_view, name="logout"),
]
