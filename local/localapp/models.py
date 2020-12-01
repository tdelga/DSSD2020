from django.db import models
import datetime
from django.utils import timezone


class Miembro_proyecto(models.Model):
    boss = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True,related_name="miembro_id")

class Proyecto(models.Model):
    name = models.CharField(max_length=200)
    date_of_start = models.DateTimeField(null=True)
    date_of_end = models.DateTimeField(null=True)
    miembro_id = models.ForeignKey(Miembro_proyecto , on_delete=models.CASCADE , related_name='proyecto_id', null=True)
    cantidad = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='pending')

class Protocolo(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,null=True,related_name="protocolo_id")
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200, default='pending')
    puntaje = models.IntegerField(default=0)
    orden = models.IntegerField(default=0)
    es_local = models.BooleanField(default=False)
    date_of_start = models.DateTimeField(null=True)
    date_of_end = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

class Proyecto_protocolo(models.Model):
    proyecto = models.ForeignKey(Proyecto , on_delete=models.CASCADE , related_name='proyecto_id')
    protocolo = models.ForeignKey(Protocolo , on_delete=models.CASCADE , related_name='protocolo_id')

class Actividad(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Actividades_protocolo(models.Model):
    actividad = models.ForeignKey(Actividad , on_delete=models.CASCADE , related_name='actividad_protocolo')
    protocolo = models.ForeignKey(Protocolo , on_delete=models.CASCADE , related_name='protocolo_actividad')
