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

    class Meta:
        model = Cliente
        fields = ('id','personal_id','nombre','email','telefono')

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
    disponible = serializers.CharField(required=True)
    imagen = serializers.ImageField(required=False)
    
    class Meta:
        model = Habitacion
        fields = ('id','numero','tipo','precio','disponible', 'imagen')