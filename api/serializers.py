from django.contrib.auth.models import User, Group
from api.models import Protocolo,Proyecto,Miembro_proyecto
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ProtocolosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Protocolo
        fields = ['id','name','status','puntaje','orden','es_local','date_of_start','date_of_end','author_id','proyecto_id'] 
        depth = 1

class ProyectoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Proyecto
        fields = "__all__"

class MiembroProyectoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Miembro_proyecto
        fields = "__all__"