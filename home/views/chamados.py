from django.shortcuts import render, redirect
from ..models import Chamado
from django.db.models import Q


def chamados_view(request):
    nivel_usuario = request.user.perfil.funcionario.nivel 

    if nivel_usuario == 'funcionario':
        chamados = Chamado.objects.filter(Q(funcionario_abriu=request.user.perfil.funcionario) | Q(setor=request.user.perfil.funcionario.setor)).order_by('-data_abertura')
    elif nivel_usuario == 'adm':
        chamados = Chamado.objects.filter(funcionario_abriu__setor=request.user.perfil.funcionario.setor) | Q(setor=request.user.perfil.funcionario.setor)#.order_by('-data_abertura')
    else:
        chamados = Chamado.objects.all().order_by('-data_abertura')

    print(len(chamados))
    return render(request, 'home/chamados/chamados.html', context={'agendamentos': chamados})


def edita_chamado(request, chamado_id):
    print(chamado_id)
    return redirect('home:home')


def deleta_chamado(request, chamado_id):

    return redirect('home:chamados')