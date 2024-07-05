from django.urls import path
from .views import * 

app_name = 'home'

urlpatterns = [
    path('', home_view, name='home'),
    path('chamados/', chamados_view, name='chamados_view'),
    # path('chamados/<int:chamado_id>', home_view, name='home'),
    path('chamados/abrir_chamado/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path("logout/", logout_view, name="logout"),
]
