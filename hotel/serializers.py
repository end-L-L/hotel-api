from rest_framework import serializers
from django.contrib.auth.models import User

from hotel.models import *

class UserSerializer(serializers.ModelSerializer):
    
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

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