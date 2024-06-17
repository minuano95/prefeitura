from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

@login_required(login_url='login/')
def home_view(request):
    return render(request, 'home/home.html')