from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProyectoForm
from .forms import ProtocoloForm
from .models import Protocolo
from .models import Proyecto_protocolo
from .models import Proyecto
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login,views as auth_views
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse,HttpResponse
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
        proyecto = Proyecto.objects.filter(name=request.POST["name"])[0]
        x=requests.post("https://dssddjango.herokuapp.com/api/token/",json={"username":"root","password":"root"})
        token = x.json()['access']
        


        cookies={
        'X-Bonita-API-Token':request.session['xbonita'],
        'BOS_Locale':request.session['boslocale'],
        'JSESSIONID':request.session['session'],
        'bonita.tenant':request.session['bonita.tenant']}
        x = requests.get("http://localhost:8080/bonita/API/bpm/process?p=0&c=1000",cookies=cookies)
        id = x.json()[0]['id']
        requests.post("http://localhost:8080/bonita/API/bpm/process/"+id+"/instantiation",headers={'X-Bonita-API-Token':request.session['xbonita']},cookies=cookies)
        nameTask = requests.get("http://localhost:8080/bonita/API/bpm/activity?p=0&c=10&f=name%3dConfiguracion del proyecto",cookies=cookies)
        caseId = nameTask.json()[0]['caseId']
        request.session['caseId'] = caseId

        x1=requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/bOS_Locale" ,cookies=cookies,json={'type':"java.lang.String",'value':request.session['boslocale']},headers={'X-Bonita-API-Token':request.session['xbonita']})
        x1=requests.get("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/bOS_Locale" ,cookies=cookies,headers={'X-Bonita-API-Token':request.session['xbonita']})
        x2=requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/bonitatenant" ,cookies=cookies,json={'type':"java.lang.String",'value':request.session['bonita.tenant']},headers={'X-Bonita-API-Token':request.session['xbonita']})
        x3=requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/jSESSIONID" ,cookies=cookies,json={'type':"java.lang.String",'value':request.session['session']},headers={'X-Bonita-API-Token':request.session['xbonita']})
        x4=requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/xBonitaAPIToken" ,cookies=cookies,json={'type':"java.lang.String",'value':request.session['xbonita']},headers={'X-Bonita-API-Token':request.session['xbonita']})
    
        headers = {"Authorization": "Bearer "+token}
        json = {
                "name":request.POST["name"],
                "cantidad":request.POST["totallength"],
                "status":"pending",
            }

        x=requests.post("https://dssddjango.herokuapp.com/proyectos/",headers=headers,json=json)
        proyecto_url=x.json()['url']
        
        rango=range(1,int(request.POST["totallength"])+1)
        for i in rango: 
            if 'es_local'+str(i) in request.POST:
                if request.POST["es_local"+str(i)] == "on":
                    es_local=True
            else:
                es_local=False
            protocolo = Protocolo(name=request.POST["name"+str(i)],orden=int(request.POST["orden"+str(i)]),es_local=es_local)
            protocolo.save()
            protocolo = Protocolo.objects.filter(name=request.POST["name"+str(i)])[0]
            if not es_local:
                json = {
                        "name":protocolo.name,
                        "es_local":False,
                        "status":"ready",
                        "orden":protocolo.orden
                    } 
            x=requests.post("https://dssddjango.herokuapp.com/protocolos/",headers=headers,json=json)
            protocolo_url=x.json()['url']
        
            x=requests.post("https://dssddjango.herokuapp.com/proyectoProtocolo/",headers=headers,json={'proyecto':proyecto_url,'protocolo':protocolo_url})
            proyecto_protocolos = Proyecto_protocolo(proyecto=proyecto,protocolo=protocolo)
            proyecto_protocolos.save()
            
        cookies={
            'X-Bonita-API-Token':request.session['xbonita'],
            'BOS_Locale':request.session['boslocale'],
            'JSESSIONID':request.session['session'],
            'bonita.tenant':request.session['bonita.tenant']}
        
        nameUser = requests.get("http://localhost:8080/bonita/API/identity/user?f=walter.bates",cookies=cookies )
        idUser = nameUser.json()[0]['id']

        nameTask = requests.get("http://localhost:8080/bonita/API/bpm/activity?p=0&c=10&f=name%3dConfiguracion del proyecto",cookies=cookies)
        idTask = nameTask.json()[0]['id']
        body = { 
                "assigned_id" : idUser, 
                "state": "completed"
                }
        requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/cantidadInstancias" ,cookies=cookies,json={'type':"java.lang.Integer",'value':int(proyecto.cantidad)},headers={'X-Bonita-API-Token':request.session['xbonita']})
        assingUser = requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'assigned_id':idUser,'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
        return redirect('inicializarProyectRender')
    else:
        form = ProyectoForm()
    return render(request, 'localapp/createProyect.html', {'formProyecto':form})

def listProyect(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'localapp/listProyect.html',{'proyectos':proyectos})

def getProtocol(request,pk):
    global proyectos_protocolos
    x=requests.post("https://dssddjango.herokuapp.com/api/token/",json={"username":"root","password":"root"})
    token = x.json()['access']

    protocolo = get_object_or_404(Protocolo,pk=pk)
    proyectoProcolo = Proyecto_protocolo.objects.filter(protocolo=pk)[0]
    proyecto = proyectoProcolo.proyecto

    if proyecto.actual == proyectoProcolo.protocolo.orden:
            
        proyecto.actual = proyecto.actual + 1

        proyecto.save()
        
        cookies={
            'X-Bonita-API-Token':request.session['xbonita'],
            'BOS_Locale':request.session['boslocale'],
            'JSESSIONID':request.session['session'],
            'bonita.tenant':request.session['bonita.tenant']}
        
        nameUser = requests.get("http://localhost:8080/bonita/API/identity/user?f=helen.kelly",cookies=cookies )
        idUser = nameUser.json()[0]['id']
        
        nameTask = requests.get("http://localhost:8080/bonita/API/bpm/activity?p=0&c=10&f=name%3dTomar protocolo",cookies=cookies)   

        idTask = nameTask.json()[0]['id']
        id = nameTask.json()[0]['caseId']
        
        if protocolo.es_local == True:
            es_local = "true"
        else:
            es_local = "false"
        requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+id+"/id" ,cookies=cookies,json={'type': "java.lang.Integer",'value':pk},headers={'X-Bonita-API-Token':request.session['xbonita']})
        requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+id+"/es_local" ,cookies=cookies,json={'type': "java.lang.Boolean",'value': es_local},headers={'X-Bonita-API-Token':request.session['xbonita']})
        requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+id+"/idProyect" ,cookies=cookies,json={'type': "java.lang.Integer",'value':proyectoProcolo.proyecto.id},headers={'X-Bonita-API-Token':request.session['xbonita']})
        requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+id+"/tokenHeroku" ,cookies=cookies,json={'type': "java.lang.String",'value':token},headers={'X-Bonita-API-Token':request.session['xbonita']})

        assingUser = requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})

        if(protocolo.es_local):
            return redirect('runProtocol',pk=pk)
        else: 
            return redirect('getProtocoloRender')
    else:
        return redirect('home')

def getProtocolRender(request):
    protocolos = Protocolo.objects.all()
    return render(request, 'localapp/getProtocol.html',{'protocolos':protocolos})


def inicializarProyect(request, id):
    cookies={
            'X-Bonita-API-Token':request.session['xbonita'],
            'BOS_Locale':request.session['boslocale'],
            'JSESSIONID':request.session['session'],
            'bonita.tenant':request.session['bonita.tenant']}
    
    
    x=requests.post("https://dssddjango.herokuapp.com/api/token/",json={"username":"root","password":"root"})
    token = x.json()['access']
    headers = {"Authorization": "Bearer "+token}
    x=requests.put("https://dssddjango.herokuapp.com/proyectos/"+str(id)+"/changeStatusProyect/running/",headers=headers)
    
    nameUser = requests.get("http://localhost:8080/bonita/API/identity/user?f=walter.bates",cookies=cookies )
    idUser = nameUser.json()[0]['id']
    nameTask = requests.get("http://localhost:8080/bonita/API/bpm/activity?p=0&c=10&f=name%3dIniciar procesamiento",cookies=cookies)
    idTask = nameTask.json()[0]['id']
    assingUser = requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'assigned_id':idUser,'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
    proyect = Proyecto.objects.get(id=id)
    proyect.status = "running"
    proyect.save()
    return redirect('home')
    

def inicializarProyectRender(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'localapp/listProyect.html',{'proyectos':proyectos})

def home(request):
    return render(request, 'localapp/home.html')

def protocolResult(request, id):
    if request.method == 'GET':
        protocol = Protocolo.objects.get(id=id)
        if protocol.status == "finished":
  
            if protocol.puntaje >= 6:
                return HttpResponse("true")
            else:
                return HttpResponse("false")

def runProtocol(request,pk):
    protocolo = get_object_or_404(Protocolo, pk=pk)
    proyectoProcolo = Proyecto_protocolo.objects.filter(protocolo=pk)[0]
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
            caseId = nameTask.json()[0]['caseId']
            protocolo.status="running"
            protocolo.puntaje = request.POST['puntaje']
            protocolo.date_of_start=datetime.now()
            protocolo.author=request.user
            protocolo.status="finished"
            protocolo.save()
            assingUser = requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'assigned_id':idUser,'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
            x=requests.get("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/resultado" ,cookies=cookies,headers={'X-Bonita-API-Token':request.session['xbonita']})
            
            proyectoProcolo = Proyecto_protocolo.objects.filter(protocolo=pk)[0]
        
            result = requests.get("http://localhost:8000/protocolResult/"+str(pk))

            if result.content.decode() == "false":
                return redirect('selectOption',pk=proyectoProcolo.proyecto.id,pkProtocol=proyectoProcolo.protocolo.id)

            return redirect('getProtocolRender')
    else:
        form = ProtocoloForm(instance=protocolo)
    return render(request, 'localapp/runProtocol.html',{'form': form,'pk':pk})



def selectOption(request,pk,pkProtocol):
    proyecto = get_object_or_404(Proyecto,pk=pk)
    
    if request.method == "POST":
        cookies={
            'X-Bonita-API-Token':request.session['xbonita'],
            'BOS_Locale':request.session['boslocale'],
            'JSESSIONID':request.session['session'],
            'bonita.tenant':request.session['bonita.tenant']}
        x=requests.post("https://dssddjango.herokuapp.com/api/token/",json={"username":"root","password":"root"})
        token = x.json()['access']
        headers = {"Authorization": "Bearer "+token}
        
        nameUser = requests.get("http://localhost:8080/bonita/API/identity/user?f=helen.kelly",cookies=cookies )
        idUser = nameUser.json()[0]['id']
        
        nameTask = requests.get("http://localhost:8080/bonita/API/bpm/activity?p=0&c=10&f=name%3dTomar accion post obtener resultado",cookies=cookies)
        caseId = nameTask.json()[0]['caseId']
        idTask = nameTask.json()[0]['id']
        
        select = request.POST["select"]
        
        protocolo = Protocolo.objects.get(id=pkProtocol)

        if  select == "canceled":
            x=requests.put("https://dssddjango.herokuapp.com/proyectos/"+str(pk)+"/changeStatusProyect/finished/",headers=headers)
            requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/select" ,cookies=cookies,json={'type': "java.lang.String",'value':"canceled"},headers={'X-Bonita-API-Token':request.session['xbonita']})
            requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'assigned_id':idUser,'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
            proyecto.status = "finished"
            proyecto.save()
            return redirect('home')
        elif select == "resetProyect":
            x=requests.put("https://dssddjango.herokuapp.com/proyectos/"+str(pk)+"/changeStatusProyect/pending/",headers=headers)
            requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/select" ,cookies=cookies,json={'type': "java.lang.String",'value':"resetProyect"},headers={'X-Bonita-API-Token':request.session['xbonita']})
            requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'assigned_id':idUser,'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
            proyecto.status = "pending"
            proyecto.actual = 1
            proyecto.save()
            return redirect('home')
        elif select == "continue":
            x=requests.post("https://dssddjango.herokuapp.com/proyectos/"+str(pk)+"/changeStatusProyect/running/",headers=headers)
            requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/select" ,cookies=cookies,json={'type': "java.lang.String",'value':"continue"},headers={'X-Bonita-API-Token':request.session['xbonita']})
            requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'assigned_id':idUser,'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
            proyecto.status = "running"
            proyecto.save()
            return redirect('inicializarProyectRender')
        elif select == "resetProtocol":
            x=requests.post("https://dssddjango.herokuapp.com/protocolos/"+str(protocolo.id)+"/changeStatusProtocol/pending//",headers=headers)
            requests.put("http://localhost:8080/bonita/API/bpm/caseVariable/"+caseId+"/select" ,cookies=cookies,json={'type': "java.lang.String",'value':"resetProtocol"},headers={'X-Bonita-API-Token':request.session['xbonita']})
            requests.put("http://localhost:8080/bonita/API/bpm/humanTask/"+idTask ,cookies=cookies,json={'assigned_id':idUser,'state':'completed'},headers={'X-Bonita-API-Token':request.session['xbonita']})
            protocolo.status = "pending"
            proyecto.actual = proyecto.actual-1
            proyecto.save()
            protocolo.save()
            return redirect('getProtocolRender')
    else: 
        return render(request,'localapp/selectOption.html',{'proyecto':proyecto,'pkProtocol':pkProtocol})
        

def finishResult(request,pk):
    protocolo = get_object_or_404(Protocolo,pk=pk)
    if(protocolo):
        protocolo.status = "finished"
        protocolo.save()
    return redirect(redirect('home'))
       


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


    #x=requests.post("https://dssddjango.herokuapp.com/api/token/",json={"username":"root","password":"root"})
    
    #headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA2OTM0ODI3LCJqdGkiOiI4N2UyZjZiYjA4NmQ0MmZkOGQyMzc1YzlhMWU0M2IwMSIsInVzZXJfaWQiOjF9.Tp9snW0m_5E_P1O_oivCmqOMPK5jTX2USd4Oo7CDF7E"}
    #y=requests.get("https://dssddjango.herokuapp.com/protocolos/",headers=headers)
    

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

def checkProtocolsPending(request, id):
    if request.method == 'GET':
        proyecto_protocolo = Proyecto_protocolo.objects.filter(protocolo=id)
        protocol = proyecto_protocolo[0].protocolo
        proyect = proyecto_protocolo[0].proyecto
        if proyect.cantidad > protocol.orden:
            return HttpResponse("true")
        return HttpResponse("false")


def readyTasks(request):
    cookies={
        'X-Bonita-API-Token':request.session['xbonita'],
        'BOS_Locale':request.session['boslocale'],
        'JSESSIONID':request.session['session'],
        'bonita.tenant':request.session['bonita.tenant']}
    
    tasks = requests.get("http://localhost:8080/bonita/API/bpm/activity?p=0&c=10",cookies=cookies)
    return render(request,"localapp/taskWithName.html",{"json":tasks.json()})

def taskWithState(request,state):
    cookies={
        'X-Bonita-API-Token':request.session['xbonita'],
        'BOS_Locale':request.session['boslocale'],
        'JSESSIONID':request.session['session'],
        'bonita.tenant':request.session['bonita.tenant']}
    
    tasks = requests.get("http://localhost:8080/bonita/API/bpm/archivedActivity?p=0&c=10&f=state="+state,cookies=cookies)
    if(state == "finished"):
        state = "finalizadas"
    else:
        state = "fallidas"
    return render(request,"localapp/taskWithState.html",{"json":tasks.json(),"state":state})



    
