from django import forms

from .models import Protocolo
from .models import Proyecto

class ProyectoForm(forms.ModelForm):

    class Meta:
        model = Proyecto
        fields = ("name","date_of_start","date_of_end")

class ProtocoloForm(forms.ModelForm):
    
    class Meta:
        model = Protocolo
        fields = ("name","orden","es_local")