from django.contrib.auth.models  import User
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from hotel.models import Cliente
from hotel.models import Habitacion
from hotel.models import Tipo_Habitacion
from hotel.models import Reservacion

from hotel.serializers import ClienteSerializer
from hotel.serializers import HabitacionSerializer
from hotel.serializers import Tipo_HabitacionSerializer
from hotel.serializers import ReservacionSerializer

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

# Habitaciones

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
        def get(self, request):
            
            habitaciones = Habitacion.objects.all()
            serializer = HabitacionSerializer(habitaciones, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

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

# Reservaciones

class CostoReservacionView(APIView):
        
    def post(self, request, *args, **kwargs):
        
        id_cliente = request.data.get("cliente")
        id_habitacion = request.data.get("habitacion")
        fecha_e = request.data.get("fecha_entrada")
        fecha_s = request.data.get("fecha_salida")
        
        if(id_cliente == 0):
            cliente = Cliente()
        else:
            cliente = get_object_or_404(Cliente, personal_id = id_cliente)
        
        habitacion = get_object_or_404(Habitacion, numero = id_habitacion)
        if not habitacion:
            return Response({"error": "Habitación no Encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        fecha_entrada = datetime.strptime(fecha_e, "%Y-%m-%d")
        fecha_salida = datetime.strptime(fecha_s, "%Y-%m-%d")

        disponible = habitacion.disponible
        dias = (fecha_salida - fecha_entrada).days

        if(dias == 0):
            dias = 1

        total = habitacion.precio * dias
        
        if cliente.descuento > 0:
            descuento = abs(cliente.descuento)

            if descuento > 1:
                descuento = descuento / 100

            total_descuento = total - (total * descuento) 
        else:
            total = habitacion.precio * dias
            total_descuento = total

        return Response({
            "mensaje": "Costo de la Reservación",
            "disponible": disponible,
            "dias": dias,
            "precio": habitacion.precio,
            "descuento": cliente.descuento,
            "total_sd": total,
            "total_cd": total_descuento
        })

class ReservacionesView(APIView):
        
    def get(self, request, *args, **kwargs):
        
        reservaciones = Reservacion.objects.all()
        serializer = ReservacionSerializer(reservaciones, many=True)
        
        return Response(serializer.data)

class ReservacionView(APIView):

    def post(self, request):
        
        # Obtener el `personal_id` del request
        personal_id = request.data.get("cliente")
        cliente = get_object_or_404(Cliente, personal_id=personal_id)
        pagado = request.data.get("pagado")

        # Crear datos para el serializador
        habitacion_id = request.data.get("habitacion")
        habitacion = get_object_or_404(Habitacion, numero=habitacion_id)
        
        fecha_entrada = datetime.strptime(request.data.get("fecha_entrada"), "%Y-%m-%d")
        fecha_salida = datetime.strptime(request.data.get("fecha_salida"), "%Y-%m-%d")
        
        # Calcular el total
        dias = (fecha_salida - fecha_entrada).days
        if dias == 0:
            dias = 1
        total = habitacion.precio * dias

        # Crear los datos para el serializador
        data = {
            "cliente": cliente.id,
            "habitacion": habitacion.id,
            "fecha_entrada": fecha_entrada.date(),
            "fecha_salida": fecha_salida.date(),
            "total": total,
            "pagado": pagado
        }

        # Pasar los datos al serializador
        reservacion = ReservacionSerializer(data=data)

        if reservacion.is_valid():
        
            if not habitacion.disponible:
                return Response({"error": "Habitación no Disponible"}, status=status.HTTP_404_NOT_FOUND)
            
            cliente.visitas += 1
            cliente.save()

            habitacion.disponible = False
            habitacion.save()

            reservacion.save()

            return Response(reservacion.data, status=201)
        
        return Response(reservacion.errors, status=400)
    
class ReservacionViewEdit(APIView):
    
    def delete(self, request, id, *args, **kwargs):
    
        id_habitacion = id
        habitacion = get_object_or_404(Habitacion, numero=id_habitacion)

        if habitacion.disponible:
            return Response({"error": "Habitación no Reservada"}, status=status.HTTP_404_NOT_FOUND)
        
        reservacion = get_object_or_404(Reservacion, habitacion=habitacion.id)
        
        if not reservacion:
            return Response({"error": "Reservación no Encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        reservacion.delete()
        habitacion.disponible = True
        habitacion.save()
        
        return Response({"message": "Reservación Eliminada"}, status=200)
    
class ListaReservacionesView(APIView):

    def get(self, request, *args, **kwargs):
        reservaciones = Reservacion.objects.select_related('cliente', 'habitacion').all()
        data = []
        for reservacion in reservaciones:
            data.append({
                "id": reservacion.id,
                "cliente": reservacion.cliente.personal_id,
                "nombre": reservacion.cliente.nombre,
                "habitacion": reservacion.habitacion.numero,
                "fecha_entrada": reservacion.fecha_entrada,
                "fecha_salida": reservacion.fecha_salida,
                "total": reservacion.total,
                "pagado": reservacion.pagado
            })
        return Response(data, status=200)
    