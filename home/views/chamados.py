from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ..models import Chamado
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def chamados_view(request):
    nivel_usuario = request.user.perfil.funcionario.nivel
    setor_usuario = request.user.perfil.funcionario.setor
    funcionario_usuario = request.user.perfil.funcionario

    if nivel_usuario == 'funcionario':
        chamados = Chamado.objects.filter(
            Q(funcionario_abriu=funcionario_usuario) | 
            Q(setor=setor_usuario) & Q(ativo=True)
        ).order_by('-data_abertura')
    elif nivel_usuario == 'adm':
        chamados = Chamado.objects.filter(
            Q(funcionario_abriu__setor=setor_usuario) | 
            Q(setor=setor_usuario) & Q(ativo=True)
        ).order_by('-data_abertura')
    else:
        chamados = Chamado.objects.filter(ativo=True).order_by('-data_abertura')

    return render(request, 'home/chamados/chamados.html', {
        'agendamentos': chamados,
        'nivel_usuario': nivel_usuario,
        'funcionario_usuario': funcionario_usuario,
        'setor_usuario': setor_usuario
    })

@login_required(login_url='/login/')
def concluir_chamado(request, chamado_id):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        chamado = get_object_or_404(Chamado, id=chamado_id)
        chamado.status = True
        chamado.descricao_solucao = descricao
        chamado.funcionario_fechou = request.user.perfil.funcionario
        chamado.data_fechamento = timezone.now()
        chamado.save()
    return redirect('home:chamados_view')

@login_required(login_url='/login/')
def edita_chamado(request, chamado_id):
    return redirect('home:home')

@login_required(login_url='/login/')
def deleta_chamado(request, chamado_id):
    return redirect('home:chamados')
