from django.contrib import admin
from .models import *

class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'precio', 'disponible')
    list_filter = ('tipo', 'disponible')

class ReservacionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'habitacion', 'fecha_entrada', 'fecha_salida')
    list_filter = ('fecha_entrada', 'fecha_salida')

admin.site.register(Administrador)
admin.site.register(Recepcionista)
admin.site.register(Cliente)
admin.site.register(Habitacion, HabitacionAdmin)
admin.site.register(Tipo_Habitacion)
admin.site.register(Reservacion, ReservacionAdmin)

