from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from ..models import Chamado, Setor, Funcionario
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models import Sum
from django.db.models import Count
from calendar import monthrange
from django.contrib.auth.decorators import login_required
from datetime import datetime
import logging
import json
from django.utils.safestring import mark_safe

def get_dados_por_mes(request):    
    # Verificar o primeiro registro financeiro
    primeiro_financeiro = Chamado.objects.order_by('data_abertura').first()
    if primeiro_financeiro is None:
        # Se não houver registros financeiros, retorne uma resposta vazia ou faça o tratamento necessário
        return render(request, 'home/estatisticas/estatisticas.html')
    
    # Verificar o último registro financeiro
    ultimo_financeiro = Chamado.objects.order_by('data_abertura').last()
    if ultimo_financeiro is None:
        # Se não houver registros financeiros, retorne uma resposta vazia ou faça o tratamento necessário
        return render(request, 'home/estatisticas/estatisticas.html')

    # Obter o ano e o mês do primeiro registro
    primeiro_ano = primeiro_financeiro.data_abertura.year
    primeiro_mes = primeiro_financeiro.data_abertura.month

    # Obter o ano e o mês do último registro
    ultimo_ano = ultimo_financeiro.data_abertura.year
    ultimo_mes = ultimo_financeiro.data_abertura.month
    
    dados_por_mes = {}

    # Loop pelos anos
    for ano in range(primeiro_ano, ultimo_ano + 1):
        # Determinar o mês inicial e final do loop baseado no ano
        mes_inicial = primeiro_mes if ano == primeiro_ano else 1
        mes_final = ultimo_mes if ano == ultimo_ano else 12

        # Loop pelos meses
        for mes in range(mes_inicial, mes_final + 1):
            # Calcular o primeiro e o último dia do mês
            primeiro_dia = timezone.make_aware(datetime(ano, mes, 1))
            ultimo_dia = timezone.make_aware(datetime(ano, mes, monthrange(ano, mes)[1], 23, 59, 59))

            # Filtrar os registros financeiros para o mês atual
            registros_do_mes = Chamado.objects.filter(
                data_abertura__gte=primeiro_dia,
                data_abertura__lt=ultimo_dia + timezone.timedelta(days=1),
                ativo=True
            )

            total_abertos = registros_do_mes.count()

            # Contar os chamados fechados no mês
            total_fechados = registros_do_mes.filter(Q(status=True) & Q(ativo=True)).count()  # Supondo que o status 'fechado' indica chamados fechados

            # Contar os chamados ainda abertos no mês
            total_em_aberto = registros_do_mes.filter(Q(status=False) & Q(ativo=True)).count()  # Supondo que o status 'aberto' indica chamados em aberto

            # Adicionar os dados ao dicionário
            if ano not in dados_por_mes:
                dados_por_mes[ano] = {}
            dados_por_mes[ano][mes] = {
                'total_abertos': total_abertos,
                'total_fechados': total_fechados,
                'total_em_aberto': total_em_aberto,
            }

    return dados_por_mes


def get_top_sectors_and_employees(request):
    # Top 3 setores que mais abrem chamados
    setores_mais_abrem_ids = Chamado.objects.values('setor').annotate(total_abertos=Count('id')).order_by('-total_abertos')[:3]
    setores_mais_abrem = [
        {
            'setor': Setor.objects.get(id=s['setor']),
            'total_abertos': s['total_abertos']
        }
        for s in setores_mais_abrem_ids
    ]
    
    # Top 3 setores que mais recebem chamados
    setores_mais_recebem_ids = Chamado.objects.values('setor').annotate(total_recebidos=Count('id')).order_by('-total_recebidos')[:3]
    setores_mais_recebem = [
        {
            'setor': Setor.objects.get(id=s['setor']),
            'total_recebidos': s['total_recebidos']
        }
        for s in setores_mais_recebem_ids
    ]
    
    # Top 3 funcionários que mais abrem chamados
    funcionarios_mais_abrem_ids = Chamado.objects.values('funcionario_abriu').annotate(total_abertos=Count('id')).order_by('-total_abertos')[:3]
    funcionarios_mais_abrem = [
        {
            'funcionario': Funcionario.objects.get(id=f['funcionario_abriu']),
            'total_abertos': f['total_abertos']
        }
        for f in funcionarios_mais_abrem_ids
    ]
    
    # Top 3 funcionários que mais fecham chamados
    funcionarios_mais_fecham_ids = Chamado.objects.filter(status=True).values('funcionario_fechou').annotate(total_fechados=Count('id')).order_by('-total_fechados')[:3]
    funcionarios_mais_fecham = [
        {
            'funcionario': Funcionario.objects.get(id=f['funcionario_fechou']),
            'total_fechados': f['total_fechados']
        }
        for f in funcionarios_mais_fecham_ids
    ]

    return {
        'setores_mais_abrem': setores_mais_abrem,
        'setores_mais_recebem': setores_mais_recebem,
        'funcionarios_mais_abrem': funcionarios_mais_abrem,
        'funcionarios_mais_fecham': funcionarios_mais_fecham,
    }

def estatisticas_view(request):
    dados_por_mes = get_dados_por_mes(request)
    top_dados = get_top_sectors_and_employees(request)

    setores_mais_abrem = json.dumps([(data["setor"].nome, data["total_abertos"]) for data in top_dados["setores_mais_abrem"]])
    setores_mais_recebem = json.dumps([(data["setor"].nome, data["total_recebidos"]) for data in top_dados["setores_mais_recebem"]])
    funcionarios_mais_abrem = json.dumps([(data["funcionario"].nome, data["total_abertos"]) for data in top_dados["funcionarios_mais_abrem"]])
    funcionarios_mais_fecham = json.dumps([(data["funcionario"].nome, data["total_fechados"]) for data in top_dados["funcionarios_mais_fecham"]])

    context = {
        'dados_por_mes': dados_por_mes,
        'top_setores_abrem': mark_safe(setores_mais_abrem),
        'top_setores_recebem': mark_safe(setores_mais_recebem),
        'top_funcionarios_abrem': mark_safe(funcionarios_mais_abrem),
        'top_funcionarios_fecham': mark_safe(funcionarios_mais_fecham),
    }

    return render(request, 'home/estatisticas/estatisticas.html', context)