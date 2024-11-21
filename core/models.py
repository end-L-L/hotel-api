from rest_framework.authentication import TokenAuthentication

# Modelo de Autenticación

class BearerTokenAuthentication(TokenAuthentication):
    keyword = u"Bearer"