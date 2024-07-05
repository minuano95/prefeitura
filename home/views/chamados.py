from django.shortcuts import render

def chamados_view(request):
    return render(request, 'home/chamados/chamados.html')