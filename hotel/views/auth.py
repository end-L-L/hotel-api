from hotel.models import *
from hotel.serializers import *

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

class CustomAuthTokenView(ObtainAuthToken):
 
    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
              
        if user.is_active:
            
            roles = user.groups.all()
            role_names = []
            
            for role in roles:
                role_names.append(role.name)
            
            role_names = role_names[0]

            token, created = Token.objects.get_or_create(user=user)
            
            if role_names == 'administrador':
                user = UserSerializer(user, many=False).data
                user['token'] = token.key
                user["role"] = "administrador"
               
                return Response(user,200)
            
            if role_names == 'recepcionista':
                user = UserSerializer(user, many=False).data
                user['token'] = token.key
                user["role"] = "recepcionista"
               
                return Response(user,200)

            else:
                return Response({"details":"Forbidden"},403)
    
        return Response({}, status=status.HTTP_403_FORBIDDEN)
    
class CustomLogoutView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):

        user = request.user
        if user.is_active:
            token = Token.objects.get(user=user)
            token.delete()

            return Response({'logout':True})

        return Response({'logout': False})