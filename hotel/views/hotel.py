from django.contrib.auth.models  import User
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from hotel.models import Cliente
from hotel.models import Habitacion
from hotel.models import Tipo_Habitacion

from hotel.serializers import ClienteSerializer
from hotel.serializers import HabitacionSerializer
from hotel.serializers import Tipo_HabitacionSerializer

from rest_framework import permissions

# Clientes

class ClientesView(APIView):
        
        #permission_classes = (permissions.IsAuthenticated,)
        def get(self, request, *args, **kwargs):
            
            clientes = Cliente.objects.all()
            serializer = ClienteSerializer(clientes, many=True)
            
            return Response(serializer.data)
        
class ClienteView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        cliente = get_object_or_404(Cliente, id = request.GET.get("id"))
        cliente = ClienteSerializer(cliente, many=False).data

        return Response(cliente, 200)
    
    def post(self, request, *args, **kwargs):
            
            cliente = ClienteSerializer(data=request.data)
            
            if cliente.is_valid():
                cliente.save()
                return Response(cliente.data, 201)
            
            return Response(cliente.errors, status=status.HTTP_400_BAD_REQUEST)

class TipoHabitacionView(APIView):
    
    permission_classes = ()
    def get(self, request, *args, **kwargs):
        
        tipo_habitaciones = Tipo_Habitacion.objects.all()
        serializer = Tipo_HabitacionSerializer(tipo_habitaciones, many=True)
        
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        
        tipo_habitacion = Tipo_HabitacionSerializer(data=request.data)
        
        if tipo_habitacion.is_valid():
            tipo_habitacion.save()
            return Response(tipo_habitacion.data, 201)
        
        return Response(tipo_habitacion.errors, status=status.HTTP_400_BAD_REQUEST)

class HabitacionesView(APIView):
        
        permission_classes = ()
        def get(self, request, *args, **kwargs):
            
            habitaciones = Habitacion.objects.all()
            serializer = HabitacionSerializer(habitaciones, many=True)
            
            return Response(serializer.data)

class HabitacionView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        habitacion = get_object_or_404(Habitacion, id = request.GET.get("id"))
        habitacion = HabitacionSerializer(habitacion, many=False).data

        return Response(habitacion, 200)
    
    def post(self, request, *args, **kwargs):
        
        habitacion = HabitacionSerializer(data=request.data)
        
        if habitacion.is_valid():
            habitacion.save()
            return Response(habitacion.data, 201)
        
        return Response(habitacion.errors, status=status.HTTP_400_BAD_REQUEST)