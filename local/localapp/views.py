from django.shortcuts import render
from .forms import ProyectoForm
from .forms import ProtocoloForm

def index(request):
    formProyecto = ProyectoForm()
    formProtocolo = ProtocoloForm()
    return render(request, 'localapp/index.html', {'formProyecto':formProyecto,'formProtocolo':formProtocolo})
