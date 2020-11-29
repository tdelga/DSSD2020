from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createProyect', views.createProyect, name='createProyect'),
    path('listProyect', views.listProyect, name='listProyect'),
    path('login',views.login,name='login'),
    path('getProtocol',views.getProtocol,name='getProtocol'),
    path('runProtocol/<int:pk>',views.runProtocol,name='runProtocol'),
    path('selectOption/<int:pk>',views.selectOption,name="selectOption"),
    path('inicializarProyect/<int:id>',views.inicializarProyect,name='inicializarProyect')
]