from rest_framework import serializers
from django.contrib.auth.models import User

from hotel.models import *

# User Serializers

class UserSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

# App Users Serializers

class AdministradorSerializer(serializers.ModelSerializer):
    
    user=UserSerializer(read_only=True)
    
    class Meta:
        model = Administrador
        fields = '__all__'


class RecepcionistaSerializer(serializers.ModelSerializer):
    
    user=UserSerializer(read_only=True)
    
    class Meta:
        model = Recepcionista
        fields = '__all__'

# Hotel Serializers

class ClienteSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField(read_only=True)
    personal_id = serializers.CharField(required=True)
    nombre = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    telefono = serializers.CharField(required=True)
    tipo_cliente = serializers.CharField(required=False)
    descuento = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Cliente
        fields = ('id','personal_id','nombre','email','telefono', 'tipo_cliente', 'descuento')

class Tipo_HabitacionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    tipo = serializers.CharField(required=True)
    descripcion = serializers.CharField(required=True)
    imagen = serializers.ImageField(required=False)

    class Meta:
        model = Tipo_Habitacion
        fields = ('id', 'tipo', 'descripcion', 'imagen')

class HabitacionSerializer(serializers.ModelSerializer):
        
    id = serializers.IntegerField(read_only=True)

    numero = serializers.IntegerField(required=True)
    tipo = serializers.PrimaryKeyRelatedField(queryset=Tipo_Habitacion.objects.all())
    precio = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    disponible = serializers.BooleanField(required=True)
    imagen = serializers.ImageField(required=False)
    
    class Meta:
        model = Habitacion
        fields = ('id','numero','tipo','precio','disponible', 'imagen')

class ReservacionSerializer(serializers.ModelSerializer):
        
    id = serializers.IntegerField(read_only=True)

    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    habitacion = serializers.PrimaryKeyRelatedField(queryset=Habitacion.objects.all())
    fecha_entrada = serializers.DateField(required=True)
    fecha_salida = serializers.DateField(required=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    pagado = serializers.BooleanField(required=False)
    
    class Meta:
        model = Reservacion
        fields = ('id','cliente','habitacion','fecha_entrada','fecha_salida', 'total', 'pagado')