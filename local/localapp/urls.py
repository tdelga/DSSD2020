from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listProyect', views.listProyect, name='listProyect'),
    path('login',views.LoginView.as_view(),name='login'),
    path('logout',views.LogoutView.as_view(),name='logout'),
    path('getProtocol',views.getProtocol,name='getProtocol'),
    path('inicializarProyect/<int:id>',views.inicializarProyect,name='inicializarProyect')
]