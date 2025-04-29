import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import SiteUser


class JwtAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:         # check header validation
            return None
        if not auth_header.startswith('Bearar '):
            return None
        
        token = auth_header.split(' ')[1]
        try:        # check token
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        
        try:    # check user exist
            user = SiteUser.objects.get(id=payload['user_id'])
        except SiteUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)
