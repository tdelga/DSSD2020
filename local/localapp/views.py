from django.shortcuts import render
from .forms import ProyectoForm
from .forms import ProtocoloForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from localapp.models import Proyecto
# models
from django.contrib.auth.models import User

def index(request):
    formProyecto = ProyectoForm()
    formProtocolo = ProtocoloForm()
    return render(request, 'localapp/index.html', {'formProyecto':formProyecto,'formProtocolo':formProtocolo})

def listProyect(request):
    return render(request, 'localapp/listProyect.html',{})

def getProtocol(request):
    return render(request, 'localapp/getProtocol.html',{})

def inicializarProyect(request, id):
    print(id)
    proyect = Proyecto.objects.get(id=id)
    proyect.status = "running"
    proyect.save()
    return render(request, 'localapp/listProyect.html',{})


class LoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    template_name = 'localapp/login.html'

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    template_name = 'localapp/logged_out.html'

