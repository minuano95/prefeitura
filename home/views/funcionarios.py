from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse
from ..forms import ChamadoForm
from ..models import Chamado, Funcionario
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
import logging

logger = logging.getLogger('main')


@login_required(login_url='/login/')
@permission_required('home.view_funcionario', raise_exception=True)
def funcionarios_view(request):
    funcionarios = Funcionario.objects.filter(status=True)   
    return render(request, 'home/funcionarios/funcionarios.html', context={'funcionarios': funcionarios})

@login_required(login_url='/login/')
@permission_required('home.edit_funcionario', raise_exception=True)
def edita_funcionario(request, funcionario_id):
    print(funcionario_id)
    return redirect('home:funcionarios')

@login_required(login_url='/login/')
@permission_required('home.edit_funcionario', raise_exception=True)
def exclui_funcionario(request, funcionario_id):
    print(funcionario_id)
    return redirect('home:funcionarios')

