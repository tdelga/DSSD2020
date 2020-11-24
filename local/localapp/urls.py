from django.urls import path
from . import views

urlpatterns = [
    path(
        route='create_proyect',
        view=views.create_proyect,
        name='create_proyect'),
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),
    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        route='',
        view=views.index,
        name='index'
    ),
]