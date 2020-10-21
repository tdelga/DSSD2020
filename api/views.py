from django.contrib.auth.models import User, Group
from api.models import Protocolo
from rest_framework import viewsets,status,permissions
from api.serializers import UserSerializer, GroupSerializer , ProtocolosSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import json
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProtocoloViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows protocols to be viewed or edited.
    """
    queryset = Protocolo.objects.all()
    serializer_class = ProtocolosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def updateProtocol(self,request, pk):
        user = request.user.id
        payload = json.loads(request.body)
        try:
            protcol_item = Protocolo.objects.filter(author=user, id=pk)
            # returns 1 or 0
            protcol_item.update(**payload)
            protcol = Protocolo.objects.get(id=pk)
            serializer = ProtocolosSerializer(protcol)
            return JsonResponse({'protocol': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



