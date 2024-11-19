from django.urls import path, include
from rest_framework import routers

from hotel.views import usuarios

routers = routers.DefaultRouter()

urlpatterns = [
    
    # administradores
    path("v1/administrador", usuarios.AdministradorView.as_view(), name="administrador"),
    path("v1/lista-administradores", usuarios.AdministradoresView.as_view(), name="lista-administradores")

]