from django import forms

from .models import Protocolo

class ProtocoloForm(forms.ModelForm):

    class Meta:
        model = Protocolo
        fields = ('author', 'proyecto','name','status','puntaje','orden','es_local','date_of_start','date_of_end')