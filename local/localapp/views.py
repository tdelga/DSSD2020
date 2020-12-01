from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProyectoForm
from .forms import ProtocoloForm
from .models import Protocolo
from .models import Proyecto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login,views as auth_views
from localapp.models import Proyecto
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib import messages
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
        proyecto = Proyecto(name=request.POST["name"],cantidad=int(request.POST["totallength"]))
        proyecto.save()
        rango=range(1,int(request.POST["totallength"])+1)
        for i in rango: 
            if request.POST["es_local"+str(i)] == "on":
                es_local=True
            else:
                es_local=False
            protocolo = Protocolo(name=request.POST["name"+str(i)],orden=int(request.POST["orden"+str(i)]),es_local=es_local)
            protocolo.save()
        cookies={
            'X-Bonita-API-Token':request.session['xbonita'],
            'BOS_Locale':request.session['boslocale'],
            'JSESSIONID':request.session['session'],
            'bonita.tenant':request.session['bonita.tenant']}
        x = requests.get("http://localhost:8080/bonita/API/bpm/process?p=0&c=1000",cookies=cookies)
        id = x.json()[0]['id']
        requests.post("http://localhost:8080/bonita/API/bpm/process/"+id+"/instantiation",headers={'X-Bonita-API-Token':request.session['xbonita']},cookies=cookies)
        
        nameUser = requests.get("http://localhost:8080/bonita/API/identity/user?f=walter.bates",cookies=cookies )
        idUser = nameUser.json()[0]['id']

        nameTask = requests.get("http://localhost:8080/bonita/API/bpm/activity?p=0&c=10&f=name%3dConfiguracion del proyecto",cookies=cookies)
        idTask = nameTask.json()[0]['id']
        body = { 
                "assigned_id" : idUser, 
                "state": "completed"
                }
        assingUser = requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'assigned_id':idUser,'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
        return redirect('createProyect')
    else:
        form = ProyectoForm()
    return render(request, 'localapp/createProyect.html', {'formProyecto':form})

def listProyect(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'localapp/listProyect.html',{'proyectos':proyectos})

def getProtocol(request,pk):
    cookies={
        'X-Bonita-API-Token':request.session['xbonita'],
        'BOS_Locale':request.session['boslocale'],
        'JSESSIONID':request.session['session'],
        'bonita.tenant':request.session['bonita.tenant']}
    nameUser = requests.get("http://localhost:8080/bonita/API/identity/user?f=helen.kelly",cookies=cookies )
    idUser = nameUser.json()[0]['id']
    nameTask = requests.get("http://localhost:8080/bonita/API/bpm/activity?p=0&c=10&f=name%3dTomar protocolo",cookies=cookies)
    idTask = nameTask.json()[0]['id']
    assingUser = requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
    id = nameTask.json()[0]['caseId']
    caseVariable = requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+id+"/id" ,cookies=cookies,json={'type': "java.lang.Integer",'value':pk},headers={'X-Bonita-API-Token':request.session['xbonita']})
    print(caseVariable.content)
    print("*"*20)
    protocolos = Protocolo.objects.all()
    print(assingUser)
    return render(request, 'localapp/getProtocol.html',{'protocolos':protocolos})

def inicializarProyect(request, id):
    cookies={
            'X-Bonita-API-Token':request.session['xbonita'],
            'BOS_Locale':request.session['boslocale'],
            'JSESSIONID':request.session['session'],
            'bonita.tenant':request.session['bonita.tenant']}
    nameUser = requests.get("http://localhost:8080/bonita/API/identity/user?f=walter.bates",cookies=cookies )
    idUser = nameUser.json()[0]['id']
    nameTask = requests.get("http://localhost:8080/bonita/API/bpm/activity?p=0&c=10&f=name%3dIniciar procesamiento",cookies=cookies)
    idTask = nameTask.json()[0]['id']
    assingUser = requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'assigned_id':idUser,'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
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
            cookies={
            'X-Bonita-API-Token':request.session['xbonita'],
            'BOS_Locale':request.session['boslocale'],
            'JSESSIONID':request.session['session'],
            'bonita.tenant':request.session['bonita.tenant']}
            nameUser = requests.get("http://localhost:8080/bonita/API/identity/user?f=helen.kelly",cookies=cookies )
            idUser = nameUser.json()[0]['id']
            nameTask = requests.get("http://localhost:8080/bonita/API/bpm/activity?p=0&c=10&f=name%3dEjecutar protocolo",cookies=cookies)
            idTask = nameTask.json()[0]['id']
            assingUser = requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'assigned_id':idUser,'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
            print(assingUser)
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
		print("protocoloResult")
		try:
			protocol = Protocolo.objects.get(id=id)
			if protocol.status == 'pending':
				return JsonResponse({'result': 'El protocolo esta en estado pendiente.'}, safe=False)
			if protocol.status == "running":
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
    body={'username': request.POST['username'],    'password':    request.POST['password'], 'redirect':'false'}
    headers={"Content-type":"application/x-www-form-urlencoded"}
    response = requests.post(URL,headers=headers,data=urllib.parse.urlencode(body))
    request.session['xbonita']=response.cookies["X-Bonita-API-Token"]
    request.session['boslocale']=response.cookies["BOS_Locale"]
    request.session['session']= response.cookies["JSESSIONID"]
    request.session['bonita.tenant']= response.cookies["bonita.tenant"]

    return response

def loginn(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login_bonita(request)
                login(request, user)
                return redirect('/')
        return redirect('home')
    form = AuthenticationForm()
    return render(request = request,template_name = "localapp/login2.html",context={"form":form})

def logout_request(request):
    logout(request)
    requests.get("http://localhost:8080/bonita/logoutservice",headers={'redirect':'false'})
    return render(request, 'localapp/home.html')
  