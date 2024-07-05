from django.contrib import admin
from .models import Setor, Funcionario, Chamados, Perfil

# Register your models here.
admin.site.register(Setor)
admin.site.register(Funcionario)
admin.site.register(Chamados)
admin.site.register(Perfil)