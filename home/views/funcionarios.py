from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse
from ..forms import FuncionarioForm
from ..models import Chamado, Funcionario
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
import logging

logger = logging.getLogger('main')


@login_required(login_url='/login/')
def funcionarios_view(request):
    funcionarios = Funcionario.objects.filter(status=True)   
    return render(request, 'home/funcionarios/funcionarios.html', context={'funcionarios': funcionarios})

@login_required(login_url='/login/')
def adiciona_funcionario(request):
    funcionario_usuario = request.user.perfil.funcionario
    print('entramos')
    if funcionario_usuario.nivel != 'funcionario':
        if request.method == "POST":
            form = FuncionarioForm(request.POST, user_level=funcionario_usuario.nivel)
            if form.is_valid():
                # funcionario = form.save(commit=False)
                # funcionario.funcionario_abriu = funcionario_usuario
                form.save()

                messages.success(request, 'Funcionário criado com sucesso.')
                return redirect('home:funcionarios')
        else:
            form = FuncionarioForm(user_level=funcionario_usuario.nivel)
        return render(request, 'home/funcionarios/adicionar_funcionario.html', {'form': form,})
    else:
        print('no else')
        messages.error(request, 'Você não tem permissão para acessar essa página.')
        print('pegou a mensagem e vai retornar')
        return redirect('home:funcionarios')

@login_required(login_url='/login/')
def edita_funcionario(request, funcionario_id):
    funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
    funcionario_usuario = request.user.perfil.funcionario

    if funcionario_usuario == funcionario or funcionario.setor == funcionario_usuario.setor and funcionario_usuario.nivel != 'funcionario' or funcionario_usuario.nivel == 'adm_sistema':
        if request.method == 'POST':
            if funcionario.setor == funcionario_usuario.setor and funcionario_usuario.nivel != 'funcionario' or funcionario_usuario.nivel == 'adm_sistema':
                form = FuncionarioForm(request.POST, instance=funcionario, user_level=funcionario_usuario.nivel)
                if form.is_valid():
                    funcionario = form.save(commit=False)
                    funcionario.save()
                    messages.success(request, 'Funcionário alterado com sucesso.')
                    return redirect('home:funcionarios')
            else:
                messages.error(request, 'Você não tem permissão para alterar o funcionário.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            form = FuncionarioForm(instance=funcionario, user_level=funcionario_usuario.nivel)

        chamados = Chamado.objects.filter(funcionario_abriu=funcionario, ativo=True).order_by('-data_abertura')
        context = {
            'funcionario': funcionario,
            'form': form,
            'agendamentos': chamados,
        }
        return render(request, 'home/funcionarios/editar_funcionario.html', context=context)
    else:
        messages.error(request, 'Você não tem permissão para acessar essa página.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

def deleta_chamado_funcionario(request, chamado_id):
    try:
        chamado = Chamado.objects.get(pk=chamado_id)
        chamado.ativo = False
        chamado.save()
        messages.success(request, 'Chamado excluído com sucesso.')
    except Chamado.DoesNotExist:    
        messages.error(request, 'Esse chamado não existe ou já foi excluído.')

    return redirect(request.META.get('HTTP_REFERER', '/'))
       
@login_required(login_url='/login/')
def exclui_funcionario(request, funcionario_id):
    try:
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
    except Funcionario.DoesNotExist:    
        messages.error(request, 'Esse funcionário não existe ou já foi excluído.')
        return redirect('home:funcionarios')

    funcionario_usuario = request.user.perfil.funcionario
    if funcionario.setor == funcionario_usuario.setor and funcionario_usuario.nivel != 'funcionario' or funcionario_usuario.nivel == 'adm_sistema':
        messages.success(request, f'{funcionario.nome} excluído com sucesso.')
        funcionario.status = False
        funcionario.save()
    else:
        messages.error(request, 'Você não tem permissão para excluir esse funcionário.')

    return redirect(request.META.get('HTTP_REFERER', '/'))

