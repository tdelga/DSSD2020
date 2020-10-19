from django.db import models
from django.utils import timezone


class Protocolo(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Actividad(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Actividades_protocolo(models.Model):
    actividad = models.ForeignKey(Actividad , on_delete=models.CASCADE , related_name='actividad_protocolo')
    protocolo = models.ForeignKey(Actividad , on_delete=models.CASCADE , related_name='protocolo_actividad')

class Miembro_proyecto(models.Model):
    name = models.CharField(max_length=200)