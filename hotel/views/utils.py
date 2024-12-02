from django.db.models import Sum
from hotel.models import Tipo_Habitacion, Habitacion, Cliente, Reservacion
from hotel.serializers import PrecioTipoHabitacionSerializer, UpdatePrecioSerializer
from hotel.serializers import DescuentoHabitualSerializer, UpdateDescuentoHabitualSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class PrecioHabitacionView(APIView):

    def get(self, request):
        tipos = Tipo_Habitacion.objects.all()
        data = []

        for tipo in tipos:
            habitaciones = Habitacion.objects.filter(tipo=tipo)

            if habitaciones.exists():
                # asumimos que todas las habitaciones del mismo tipo tienen el mismo precio
                precio = habitaciones.first().precio
            else:
                precio = None 

            serializer = PrecioTipoHabitacionSerializer({
                'tipo_id': tipo.id,
                'tipo': tipo.tipo,
                'precio': precio
            })

            data.append(serializer.data)

        return Response(data)

    def put(self, request):
        serializer = UpdatePrecioSerializer(data=request.data)
        if serializer.is_valid():
            tipo_id = serializer.validated_data['tipo_id']
            precio = serializer.validated_data['precio']

            try:
                tipo = Tipo_Habitacion.objects.get(id=tipo_id)
            except Tipo_Habitacion.DoesNotExist:
                return Response({'error': 'Tipo de Habitación no Encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            # actualizamos todas las habitaciones de este tipo con el nuevo precio
            habitaciones = Habitacion.objects.filter(tipo=tipo)
            habitaciones.update(precio=precio)

            return Response({'message': 'Precio actualizado exitosamente.'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DescuentoUsualView(APIView):

    def get(self, request):
        # obtenemos todos los clientes habituales
        clientes_habituales = Cliente.objects.filter(tipo_cliente='H')

        if clientes_habituales.exists():
            # asumimos que todos los clientes habituales tienen el mismo descuento
            descuento = clientes_habituales.first().descuento
            serializer = DescuentoHabitualSerializer({
                'tipo_cliente': 'H',
                'descuento': descuento
            })
            return Response(serializer.data)
        else:
            return Response({'error': 'No hay clientes habituales.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        serializer = UpdateDescuentoHabitualSerializer(data=request.data)
        if serializer.is_valid():
            descuento = serializer.validated_data['descuento']

            # actualizamos el 'descuento' para todos los clientes habituales
            updated = Cliente.objects.filter(tipo_cliente='H').update(descuento=descuento)

            return Response({
                'message': f'Descuento Actualizado para {updated} Clientes Habituales.'
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def calcular_ganancias(mes, anio):
    """
    Calcula las ganancias totales de un mes y año específicos.
    :param mes: Mes (1 a 12)
    :param anio: Año (ejemplo: 2024)
    :return: Total de ganancias (float)
    """
    if not (1 <= mes <= 12):
        raise ValueError("El 'mes' Debe Estar Entre 1 y 12.")
    if anio < 1:
        raise ValueError("El 'anio' Debe ser un Número Positivo.")

    # filtrar reservaciones que coincidan con el mes y año y estén pagadas
    reservaciones_mes = Reservacion.objects.filter(
        fecha_entrada__month=mes,
        fecha_entrada__year=anio,
        pagado=True
    )

    # sumar los totales
    ganancias = reservaciones_mes.aggregate(total_ganancias=Sum('total'))['total_ganancias']

    return ganancias or 0.0  # devuelve 0 si no hay resultados

class GananciasView(APIView):
    """
    API View para calcular las ganancias de un mes y año específicos.
    """

    def post(self, request):
        """
        Maneja solicitudes POST para calcular las ganancias.
        Espera un cuerpo JSON con 'mes' y 'anio'.
        """
        mes = request.data.get('mes')  # mes en formato numérico (1-12)
        anio = request.data.get('anio')  # año en formato numérico

        if mes is None or anio is None:
            return Response(
                {"error": "Se Requieren los Campos 'mes' y 'anio'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # llamar a la función de utilidades
            ganancias = calcular_ganancias(mes, anio)

            return Response(
                {"mes": mes, "anio": anio, "ganancias": ganancias},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Error Inesperado: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
