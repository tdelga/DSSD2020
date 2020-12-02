from django.urls import include, path
from rest_framework import routers
from api import views
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'protocolos', views.ProtocoloViewSet)
router.register(r'miembroProyecto', views.MiembroProyectoViewSet)
router.register(r'proyectoProtocolo', views.ProyectoProtocoloViewSet)
router.register(r'proyecto',views.ProyectoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  
    path('createProtocol/<int:pk_project>/<int:pk>/', views.createProtocol)
]

