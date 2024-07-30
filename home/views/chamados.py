from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ..models import Chamado
from ..forms import ChamadoForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def chamados_view(request):
    nivel_usuario = request.user.perfil.funcionario.nivel
    setor_usuario = request.user.perfil.funcionario.setor
    funcionario_usuario = request.user.perfil.funcionario

    if nivel_usuario == 'funcionario':
        chamados = Chamado.objects.filter(
            Q(funcionario_abriu=funcionario_usuario) & Q(ativo=True) | 
            Q(setor=setor_usuario) & Q(ativo=True)
        ).order_by('-data_abertura')
    elif nivel_usuario == 'adm':
        chamados = Chamado.objects.filter(
            Q(funcionario_abriu__setor=setor_usuario) & Q(ativo=True) | 
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
    
    messages.success(request, 'Chamado concluído com sucesso.')
    return redirect('home:chamados_view')

@login_required(login_url='/login/')
def abrir_chamado(request):
    funcionario_usuario = request.user.perfil.funcionario
    if request.method == "POST":
        form = ChamadoForm(request.POST)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.funcionario_abriu = funcionario_usuario
            chamado.save()

            messages.success(request, 'Chamado aberto com sucesso.')
            return redirect('home:chamados_view')
    else:
        form = ChamadoForm()
    return render(request, 'home/chamados/abrir_chamado.html', {'form': form,})
        
@login_required(login_url='/login/')
def reabrir_chamado(request, chamado_id):
    if request.method == 'POST':
        # descricao = request.POST.get('descricao')
        chamado = get_object_or_404(Chamado, id=chamado_id)
        chamado.status = False
        chamado.descricao_solucao = ''
        chamado.funcionario_fechou = None
        chamado.data_fechamento = None
        chamado.save()
        messages.success(request, 'O chamado foi reaberto.')
    return redirect('home:chamados_view')

@login_required(login_url='/login/')
def edita_chamado(request, chamado_id):
    funcionario_usuario = request.user.perfil.funcionario
    try:
        chamado = get_object_or_404(Chamado, pk=chamado_id)
    
        if request.method == "POST":
            form = ChamadoForm(request.POST, instance=chamado)
            if form.is_valid():
                form.save()
                messages.success(request, 'Chamado alterado com sucesso.')
                return redirect('home:chamados_view')
        else:
            form = ChamadoForm(instance=chamado)
            if chamado.funcionario_abriu == funcionario_usuario or chamado.funcionario_abriu.setor == funcionario_usuario.setor and funcionario_usuario.nivel != 'funcionario' or funcionario_usuario.nivel == 'adm_sistema':
                return render(request, 'home/chamados/editar_chamado.html', {'form': form, 'chamado': chamado, 'nivel_usuario': funcionario_usuario.nivel})
            else:
                messages.error(request, 'Você não tem permissão para acessar essa página.')
    except Chamado.DoesNotExist:
        messages.error(request, 'Esse chamado não existe ou já foi excluído.')
        
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='/login/')
def deleta_chamado(request, chamado_id):
    funcionario_usuario = request.user.perfil.funcionario
    if request.method == 'POST':
        if chamado.funcionario_abriu == funcionario_usuario or chamado.funcionario_abriu.setor == funcionario_usuario.setor and funcionario_usuario.nivel != 'funcionario' or funcionario_usuario.nivel == 'adm_sistema':
            chamado = get_object_or_404(Chamado, id=chamado_id)
            chamado.ativo = False
            chamado.save()
            messages.success(request, 'Chamado excluído com sucesso.')
        else:
            messages.error(request, 'Você não tem permissão para excluir esse chamado.')
    return redirect('home:chamados_view')
