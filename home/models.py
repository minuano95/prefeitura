from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Setor(models.Model):
    nome = models.CharField(max_length=30)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.id} | {self.nome}'

class Funcionario(models.Model):
    NIVEIS = [
        ('adm_sistema', 'Administrador do Sistema'),
        ('adm', 'Administrador do Setor'),
        ('funcionario', 'Funcionário'),
    ]

    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=20)
    telefone = PhoneNumberField(default='+55', region='BR')
    email = models.EmailField()
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, limit_choices_to={'status': True})
    nivel = models.CharField(max_length=25, choices=NIVEIS)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.id} | {self.setor} | {self.nome}'
    
class Chamados(models.Model):
    descricao = models.CharField(max_length=280)
    funcionario_abre = models.ForeignKey(Funcionario, on_delete=models.CASCADE, limit_choices_to={'status': True})
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, limit_choices_to={'status': True})
    status = models.BooleanField(default=True)
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_limite = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.id} | {self.setor} | {self.data_abertura}'