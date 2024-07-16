from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Setor(models.Model):
    nome = models.CharField(max_length=30)
    recebe_chamado = models.BooleanField(default=True)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.nome}'
    
class AreaSetor(models.Model):
    nome = models.CharField(max_length=30)
    setor = setor = models.ForeignKey(Setor, on_delete=models.CASCADE, limit_choices_to={'status': True})
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.nome}'

class Funcionario(models.Model):
    NIVEIS = [
        ('adm_sistema', 'Administrador do Sistema'),
        ('adm', 'Administrador do Setor'),
        ('funcionario', 'Funcionário'),
    ]

    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=20)
    telefone = PhoneNumberField(default='+55', region='BR')
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, limit_choices_to={'status': True})
    area_setor = models.ForeignKey(AreaSetor, on_delete=models.CASCADE, limit_choices_to={'status': True})
    nivel = models.CharField(max_length=25, choices=NIVEIS)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.setor} - {self.nome}'
    
class Chamado(models.Model):
    descricao = models.CharField(max_length=280)
    funcionario_abriu = models.ForeignKey(Funcionario, on_delete=models.CASCADE, limit_choices_to={'status': True}, related_name='chamados_abertos')
    funcionario_fechou = models.ForeignKey(Funcionario, on_delete=models.CASCADE, limit_choices_to={'status': True}, related_name='chamados_fechados', blank=True, null=True)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, limit_choices_to={'status': True, 'recebe_chamado': True,})
    status = models.BooleanField(default=False)
    descricao_solucao = models.CharField(max_length=280, default='', blank=True, null=True)
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.id} - {self.setor} - {self.data_abertura}'
    

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    # Outros campos do perfil, se necessário

    def __str__(self):
        return self.user.username
