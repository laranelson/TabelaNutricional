from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as app_login, logout as app_logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(TemplateView):
    template_name = 'core/index.html'

class AppView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    template_name = 'core/app.html'
    

def login(request):
    return render(request, "core/login.html")

def submit_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            app_login(request, user)
            return redirect("app")
        else:
            messages.error(request, "Usuário/Senha Inválido. Por favor tente novamente")
    return redirect("login")

def logout(request):
    app_logout(request)
    return redirect("index")