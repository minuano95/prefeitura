from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from ..forms import LoginForm

def login_view(request):
    if request.method == "POST":
        loginForm = LoginForm(request, data=request.POST)

        user = loginForm['username'].value()
        password = loginForm['password'].value()

        if loginForm.is_valid():
            user = loginForm.get_user()
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home:home')

    return render(request, 'home/accounts/accounts.html', context={'form': LoginForm})

def logout_view(request):
    logout(request)
    return redirect('home:login')