from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from ..models import setor
from ..forms import setorForm
from django.contrib.auth.decorators import login_required, permission_required
import logging

logger = logging.getLogger('main')

@login_required(login_url='/login/')
@permission_required('home.view_funcionario', raise_exception=True)
def setores_view(request):
    funcionario_usuario = request.user.perfil.funcionario
    setores = setor.objects.filter(status=True)
    return render(request, 'home/setores/setores.html', context={'setores': setores})

@login_required(login_url='/login/')
@permission_required('home.view_funcionario', raise_exception=True)
def adiciona_setor(request):
    home_usuario = request.user.perfil.home
    form = setorForm()
    
    if request.method == 'POST':
        form = setorForm(request.POST)
        if form.is_valid():
            setor = form.save(commit=False)
            setor.home = home_usuario 
            setor.save()
            logger.info(f'setor Criado | setor: {setor} | Usuário: {home_usuario}')
            return redirect('home:setores')
        else:
            form = setorForm()
            logger.warning(f'{form.errors}')
    return render(request, 'home/setores/adiciona_setor.html', context={'form': form})

@login_required(login_url='/login/')
@permission_required('home.view_funcionario', raise_exception=True)
def edita_setor(request, setor_id):
    home_usuario = request.user.perfil.home
    setor = get_object_or_404(setor, id=setor_id)

    if setor.home != home_usuario:
        raise Http404

    setor.tempo_necessario = str(setor.tempo_necessario).split(':')[-1]

    if request.method == 'POST':
        form = setorForm(request.POST, instance=setor)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.home = home_usuario
            horario.save()
            logger.info(f'Horário de atendimento Editado | Horario Atendimento: {setor} | Usuário: {home_usuario}')
            return redirect('home:setores')
    else:
        form = setorForm(instance=setor)
    return render(request, 'home/setores/edita_setor.html', {'form': form, 'setor_id': setor_id})

@login_required(login_url='/login/')
@permission_required('home.view_funcionario', raise_exception=True)
def exclui_setor(request, setor_id):
    home_usuario = request.user.perfil.home
    setor = get_object_or_404(setor, pk=setor_id, home=home_usuario)

    if setor.home != home_usuario:
        raise Http404
    
    setor.delete()
    logger.info(f'Horário de atendimento excluido | Horario Atendimento: {setor} | Usuário: {home_usuario}')

    return redirect('home:setores')