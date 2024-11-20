from django.urls import path, include
from rest_framework import routers

from hotel.views import auth
from hotel.views import usuarios

routers = routers.DefaultRouter()

urlpatterns = [

    # auth - login and logout
    path("v1/login", auth.CustomAuthTokenView.as_view(), name="login"),
    path("v1/logout", auth.CustomLogoutView.as_view(), name="logout"),

    # administradores
    path("v1/administrador", usuarios.AdministradorView.as_view(), name="administrador"),
    path("v1/lista-administradores", usuarios.AdministradoresView.as_view(), name="lista-administradores"),

    # recepcionistas
    path("v1/recepcionista", usuarios.RecepcionistaView.as_view(), name="recepcionista"),
    path("v1/lista-recepcionistas", usuarios.RecepcionistasView.as_view(), name="lista-recepcionistas")
]