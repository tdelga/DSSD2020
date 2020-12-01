from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createProyect', views.createProyect, name='createProyect'),
    path('listProyect', views.listProyect, name='listProyect'),
    path('login', views.loginn, name='login'),
    path('loginB',views.login_bonita , name='login_bonita'),
    path('logout', views.logout_request, name='logout'),
    path('getProtocol/<int:pk>',views.getProtocol,name='getProtocol'),
    path('runProtocol/<int:pk>',views.runProtocol, name='runProtocol'),
    path('selectOption/<int:pk>',views.selectOption, name="selectOption"),
    path('inicializarProyect/<int:id>',views.inicializarProyect, name='inicializarProyect'),
    path('protocolResult/<int:id>', views.protocolResult, name='protocolResult'),
    path('checkProtocolsPending/<int:id>', views.checkProtocolsPending, name='checkProtocolsPending'),
]