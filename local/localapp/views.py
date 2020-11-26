from django.shortcuts import render,redirect
from .forms import ProyectoForm
from .forms import ProtocoloForm
from .models import Protocolo
from .models import Proyecto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from localapp.models import Proyecto
# models
from django.contrib.auth.models import User

def createProyect(request):
    if request.method == "POST":
        proyecto = Proyecto(name=request.POST["name"])
        proyecto.save()
        rango=range(1,int(request.POST["totallength"])+1)
        for i in rango:
            if request.POST["es_local"+str(i)] == "on":
                es_local=True
            else:
                es_local=False
            protocolo = Protocolo(name=request.POST["name"+str(i)],orden=int(request.POST["orden"+str(i)]),es_local=es_local)
            print(protocolo)
            protocolo.save()
        return redirect('createProyect')
    else:
        form = ProyectoForm()
    return render(request, 'localapp/createProyect.html', {'formProyecto':form})

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

def home(request):
    return render(request, 'localapp/home.html')

