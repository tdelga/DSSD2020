from django.contrib.auth.models import User, Group
from api.models import Protocolo,Miembro_proyecto,Proyecto
from rest_framework import viewsets,status,permissions
from api.serializers import UserSerializer, GroupSerializer , ProtocolosSerializer,MiembroProyectoSerializer,ProyectoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import JsonResponse
from rest_framework.test import APIRequestFactory
import datetime
import json
from django.utils import timezone
from rest_framework.request import Request
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]

class ProtocoloViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows protocols to be viewed or edited.
    """
    queryset = Protocolo.objects.all()
    serializer_class = ProtocolosSerializer
    #permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['PUT','GET'], url_path="inicializar/(?P<pk_project>[^/.]+)", url_name="update")
    def inicializar(self,request,pk,pk_project):
        
        if request.method == 'PUT':
            try:
                
                protcol_item = Protocolo.objects.get(id=pk)
                if(protcol_item.status == "executing"):
                    raise Exception("El protocolo ya esta iniciado")
                if(int(protcol_item.proyecto_id) != int(pk_project)):
                    raise Exception("El protocolo no pertenece a ese proyecto")
                protcol_item.date_of_start = datetime.datetime.now()
                protcol_item.date_of_end = datetime.datetime.now() + datetime.timedelta(minutes=15)
                protcol_item.status ="executing"
                
                protcol_item.save()    
                

                return JsonResponse({'Protocolo ': "Se inicializo correctamente"}, safe=False, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return JsonResponse({'error': "El protocolo no existe"}, safe=False, status=status.HTTP_404_NOT_FOUND)
            except Exception as er:
                return JsonResponse({'error': str(er)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.method == 'GET':
            users = Protocolo.objects.all()
            serializer = ProtocolosSerializer(users, many=True,context={'request': request})
            return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path="consulta", url_name="consulta")
    def consulta(self,request,pk):
        
        if request.method == 'GET':
            try:
                
                protcol_item = Protocolo.objects.get(id=pk)
                if(protcol_item.status == "executing"):
                    if(protcol_item.date_of_end < timezone.now()):
                        protcol_item.status ="finished"
                        protcol_item.save()    
                        return JsonResponse({'Estado del protocolo ': protcol_item.status,'Puntaje': protcol_item.puntaje}, safe=False, status=status.HTTP_200_OK)
                if(protcol_item.status == "finished"):
                    return JsonResponse({'Estado del protocolo ': protcol_item.status,'Puntaje': protcol_item.puntaje}, safe=False, status=status.HTTP_200_OK)
                return JsonResponse({'Estado del protocolo ': protcol_item.status}, safe=False, status=status.HTTP_200_OK)   

            except ObjectDoesNotExist as e:
                return JsonResponse({'error': "El protocolo no existe"}, safe=False, status=status.HTTP_404_NOT_FOUND)
            except Exception as er:
                return JsonResponse({'error': str(er)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProyectoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows protocols to be viewed or edited.
    """
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    #permission_classes = [permissions.IsAuthenticated]

class MiembroProyectoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows protocols to be viewed or edited.
    """
    queryset = Miembro_proyecto.objects.all()
    serializer_class = MiembroProyectoSerializer
    #permission_classes = [permissions.IsAuthenticated]

    

@api_view(["POST","GET"])
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
def createProtocol(request,pk_project,pk):
    if request.method == 'POST':
        payload = request.POST
        user = request.user
        try:
            author = User.objects.get(id=payload["id"])
            protocol = Protocolo.objects.create(
                name="Protocol_2",
                status= "b",
                puntaje= 4,
                orden= 1,
                es_local= False,
                date_of_start= "2012-09-04 06:00",
                date_of_end= "2012-09-04 06:00",
                author_id=1,
                proyecto_id= 1,
                author=author
            )
            serializer = ProtocolosSerializer(protocol)
            return JsonResponse({'books': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        users = Protocolo.objects.all()
        serializer = ProtocolosSerializer(users, many=True)
        return Response(serializer.data)
