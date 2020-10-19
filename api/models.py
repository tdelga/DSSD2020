from django.db import models
import datetime
from django.utils import timezone


class Protocolo(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    proyecto = models.ForeignKey('models.Proyecto', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    puntaje = models.IntegerField(default=0)
    orden = models.IntegerField(default=0)
    es_local = models.BooleanField(default=False)
    date_of_start = models.DateTimeField(default=timezone.now)
    date_of_end = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Proyecto(models.Model):
    name = models.CharField(max_length=200)
    date_of_start = models.DateTimeField(default=timezone.now)
    date_of_end = models.DateTimeField(default=timezone.now)
    responsable =  models.ForeignKey('auth.User', on_delete=models.CASCADE)


    def __str__(self):
        return self.name