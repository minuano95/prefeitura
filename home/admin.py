from django.contrib import admin
from .models import Setor, Funcionario, Chamado, Perfil, AreaSetor

# Register your models here.
admin.site.register(Setor)
admin.site.register(AreaSetor)
admin.site.register(Funcionario)
admin.site.register(Chamado)
admin.site.register(Perfil)