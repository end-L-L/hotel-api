from django.contrib import admin
from .models import *

admin.site.register(Administrador)
admin.site.register(Recepcionista)
admin.site.register(Cliente)
admin.site.register(Habitacion)
admin.site.register(Tipo_Habitacion)

