from django.urls import path, include
from rest_framework import routers

from hotel.views import auth
from hotel.views import usuarios
from hotel.views import hotel

from django.conf import settings
from django.conf.urls.static import static

routers = routers.DefaultRouter()

urlpatterns = [

    # App

    # auth - login and logout
    path("v1/login", auth.CustomAuthTokenView.as_view(), name="login"),
    path("v1/logout", auth.CustomLogoutView.as_view(), name="logout"),

    # administradores
    path("v1/administrador", usuarios.AdministradorView.as_view(), name="administrador"),
    path("v1/lista-administradores", usuarios.AdministradoresView.as_view(), name="lista-administradores"),

    # recepcionistas
    path("v1/recepcionista", usuarios.RecepcionistaView.as_view(), name="recepcionista"),
    path("v1/lista-recepcionistas", usuarios.RecepcionistasView.as_view(), name="lista-recepcionistas"),

    # Hotel

    # clientes
    path("v1/hotel/cliente", hotel.ClienteView.as_view(), name="cliente"),
    path("v1/hotel/lista-clientes", hotel.ClientesView.as_view(), name="lista-clientes"),

    # habitaciones
    path("v1/hotel/habitacion", hotel.HabitacionView.as_view(), name="habitacion"),
    path("v1/hotel/lista-habitaciones", hotel.HabitacionesView.as_view(), name="lista-habitaciones"),
	
    # tipo habitaciones
    path("v1/hotel/tipo-habitacion", hotel.TipoHabitacionView.as_view(), name="tipo-habitacion"),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)