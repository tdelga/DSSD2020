from django.shortcuts import render
from .forms import ProyectoForm
from .forms import ProtocoloForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views

# models
from django.contrib.auth.models import User

def index(request):
    formProyecto = ProyectoForm()
    formProtocolo = ProtocoloForm()
    return render(request, 'localapp/index.html', {'formProyecto':formProyecto,'formProtocolo':formProtocolo})

def listProtocol(request):
    return render(request, 'localapp/listProtocol.html',{})

def getProtocol(request):
    return render(request, 'localapp/getProtocol',{})

class LoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = 'localapp/login.html'

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'localapp/logged_out.html'

