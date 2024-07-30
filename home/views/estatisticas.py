from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ..models import Chamado
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def estatisticas_view(request):
    return render(request, 'home/estatisticas/estatisticas.html')