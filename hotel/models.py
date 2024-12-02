from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Administrador
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

# Recepcionista
class Recepcionista(models.Model):
    id = models.BigAutoField(primary_key=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    clave_recepcionista = models.CharField(max_length=128, null=True, blank=True)
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
        return f"Clave: {self.clave_recepcionista or 'N/A'}"
    
    class Meta:
        verbose_name = 'Recepcionista'
        verbose_name_plural = 'Recepcionistas'
        #ordering = ['-creation']

# Cliente
class Cliente(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    
    TIPO_CLIENTE = [
        ('H', 'Habitual'),
        ('E', 'Esporádico'),
    ]
    personal_id = models.CharField(max_length=128, unique=True, blank=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    tipo_cliente = models.CharField(max_length=1, choices=TIPO_CLIENTE, default='E')
    descuento = models.FloatField(default=0.0)
    visitas = models.IntegerField(default=0)

    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo_cliente})"
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        #ordering = ['-creation']
    
# Tipos de Habitación
class Tipo_Habitacion(models.Model):
    
    tipo = models.CharField(max_length=32)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='images/', null=True)

    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tipo {self.tipo}"
    
    class Meta:
        verbose_name = 'Tipo de Habitación'
        verbose_name_plural = 'Tipos de Habitaciones'
        #ordering = ['-creation']

# Habitaciones
class Habitacion(models.Model):
    
    id = models.BigAutoField(primary_key=True)
   
    numero = models.CharField(max_length=10, unique=True)
    tipo = models.ForeignKey(Tipo_Habitacion, on_delete=models.CASCADE)
    precio = models.FloatField()
    disponible = models.BooleanField(default=True)

    imagen = models.ImageField(upload_to='images/', null=True)

    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Habitación: {self.numero}"
    
    class Meta:
        verbose_name = 'Habitación'
        verbose_name_plural = 'Habitaciones'
        #ordering = ['+creation']

# Reservaciones
class Reservacion(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    total = models.FloatField()
    pagado = models.BooleanField(default=False)

    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservación: {self.id}"
    
    class Meta:
        verbose_name = 'Reservación'
        verbose_name_plural = 'Reservaciones'
        #ordering = ['-creation']