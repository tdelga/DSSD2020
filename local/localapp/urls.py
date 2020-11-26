from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createProyect', views.createProyect, name='createProyect'),
    path('listProyect', views.listProyect, name='listProyect'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('getProtocol',views.getProtocol,name='getProtocol'),
    path('inicializarProyect/<int:id>',views.inicializarProyect,name='inicializarProyect')
]