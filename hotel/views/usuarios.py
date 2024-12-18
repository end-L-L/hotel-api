from django.contrib.auth.models  import User
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from hotel.serializers import UserSerializer
from hotel.serializers import AdministradorSerializer
from hotel.serializers import RecepcionistaSerializer
from hotel.serializers import ClienteSerializer

from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from hotel.models import Administrador
from hotel.models import Recepcionista
from hotel.models import Cliente

# Administradores

class AdministradoresView(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        
        administradores = Administrador.objects.all()
        serializer = AdministradorSerializer(administradores, many=True)
        
        return Response(serializer.data)
        
class AdministradorView(APIView):
   
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        
        admin = get_object_or_404(Administrador, id = request.GET.get("id"))
        admin = AdministradorSerializer(admin, many=False).data

        return Response(admin, 200)
    
    permission_classes = ()
    def post(self, request, *args, **kwargs):
        
        user = UserSerializer(data=request.data)
        
        if user.is_valid():
            role = request.data['role']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            
            # valida email
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"mensaje":"Correo "+email+", ya Existe"},400)

            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)

            user.save()
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            # perfil administrador
            admin = Administrador.objects.create(user=user,
                                            clave_administrador= request.data["clave_administrador"],
                                            telefono= request.data["telefono"],
                                            rfc= request.data["rfc"].upper(),
                                            edad= request.data["edad"],
                                            ocupacion= request.data["ocupacion"])
            admin.save()

            return Response({"administrador_id": admin.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

# Recepcionistas

class RecepcionistasView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        
        recepcionistas = Recepcionista.objects.all()
        serializer = RecepcionistaSerializer(recepcionistas, many=True)
        
        return Response(serializer.data)
    
class RecepcionistaView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        
        recepcionista = get_object_or_404(Recepcionista, id = request.GET.get("id"))
        recepcionista = RecepcionistaSerializer(recepcionista, many=False).data

        return Response(recepcionista, 200)
    
    permission_classes = ()
    def post(self, request, *args, **kwargs):
        
        user = UserSerializer(data=request.data)
        
        if user.is_valid():
            role = request.data['role']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            
            # valida email
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"mensaje":"Correo "+email+", ya Existe"},400)

            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)

            user.save()
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            # perfil recepcionista
            recepcionista = Recepcionista.objects.create(user=user,
                                            clave_recepcionista= request.data["clave_recepcionista"],
                                            telefono= request.data["telefono"],
                                            rfc= request.data["rfc"].upper(),
                                            edad= request.data["edad"],
                                            ocupacion= request.data["ocupacion"])
            recepcionista.save()

            return Response({"recepcionista_id": recepcionista.id }, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)