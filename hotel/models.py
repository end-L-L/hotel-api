from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Administrador(models.Model):
    id = models.BigAutoField(primary_key=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    clave_administrador = models.CharField(max_length=128, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rfc = models.CharField(max_length=13, null=True, blank=True)
    edad = models.IntegerField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Clave: {self.clave_administrador or 'N/A'}"
    
    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'
        ordering = ['-creation']
