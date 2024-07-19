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
    path('login/', login_view, name='login'),
    path("logout/", logout_view, name="logout"),
]
