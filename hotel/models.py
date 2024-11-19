from django.db import models
from django.contrib.auth.models import User

class Administrador(models.Model):
    id = models.BigAutoField(primary_key=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    
    clave_administrador = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255,null=True, blank=True)
    
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Clave " + self.clave_administrador