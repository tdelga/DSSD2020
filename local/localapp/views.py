from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProyectoForm
from .forms import ProtocoloForm
from .models import Protocolo
from .models import Proyecto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from localapp.models import Proyecto
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth import logout
import requests
import httplib2
import json
import urllib
from json import JSONEncoder


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
    protocolos = Protocolo.objects.all()
    return render(request, 'localapp/getProtocol.html',{'protocolos':protocolos})

def inicializarProyect(request, id):
    proyect = Proyecto.objects.get(id=id)
    proyect.status = "running"
    proyect.save()
    return render(request, 'localapp/listProyect.html',{})

def home(request):
    return render(request, 'localapp/home.html')

def runProtocol(request,pk):
    protocolo = get_object_or_404(Protocolo, pk=pk)
    if request.method == "POST":
        form = ProtocoloForm(request.POST,instance=protocolo)
        if form.is_valid():
            protocolo.status="running"
            protocolo.date_of_start=datetime.now()
            protocolo.author=request.user
            protocolo.save()
            return redirect('home')
    else:
        form = ProtocoloForm(instance=protocolo)
    return render(request, 'localapp/runProtocol.html',{'form': form,'pk':pk})

def selectOption(request,pk):
    proyecto = get_object_or_404(Proyecto,pk=pk)
    if request.method == "POST":
        select = request.POST["select"]
        if  select == "canceled":
            proyecto.status = "canceled"
        elif select == "reset":
            proyecto.status = "pending"
        return redirect('home')
    return render(request,'localapp/selectOption.html',{'pk':pk})

def protocolResult(request, id):
	if request.method == 'GET':
		try:
			protocol = Protocolo.objects.get(id=id)
			if protocol.status == 'pending':
				return JsonResponse({'result': 'El protocolo esta en estado pendiente.'}, safe=False)
			if protocol.status == "executing":
				return JsonResponse({'result': 'El protocolo aun no ha finalizado.'}, safe=False)
			if protocol.status == "finished":
				if protocol.puntaje >= 6:
					result = 'positivo'
				else:
					result = 'negativo'
			return JsonResponse({'Puntaje': protocol.puntaje, 'Resultado final': result}, safe=False)
		except ObjectDoesNotExist as e:
			return JsonResponse({'error': "Protocolo inexistente"}, safe=False)
		except Exception as er:
			return JsonResponse({'error': str(er)}, safe=False)

def login_bonita(request):
	http = httplib2.Http()
	URL="http://localhost:8080/bonita/loginservice"
	body={'username': request.POST['username'],	'password':	request.POST['password']}
	headers={"Content-type":"application/x-www-form-urlencoded"}
	response, content = http.request(URL,'POST',headers=headers,body=urllib.parse.urlencode(body))
	request.session['token_bpm'] = response['set-cookie']
	print(type(response['set-cookie']))
	print("------------------------------------------------------------------")
	print(content)

def login(request):
	if request.method == "POST":
		login_bonita(request)
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect('/')
			else:
				messages.error(request, "Invalid username or password.")
		else:
			messages.error(request, "Invalid username or password.")
		return redirect('home')
	form = AuthenticationForm()
	return render(request = request,
					template_name = "localapp/login.html",
					context={"form":form})

def logout_request(request):
    logout(request)
    return render(request, 'localapp/home.html')
