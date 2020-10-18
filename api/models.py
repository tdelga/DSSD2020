from django.db import models
from django.utils import timezone


class Protocolo(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.name