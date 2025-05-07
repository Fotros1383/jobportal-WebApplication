from datetime import datetime
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import SiteUser
from django.http import HttpResponseRedirect
import jwt 
from rest_framework.request import HttpRequest
login_attempts = {}

class JwtAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request:HttpRequest):
        print("meow")
        token = request.COOKIES.get('user_token')
        print('token is:',token)
        if isinstance(token, bytes):
            print('we are here')
            token = token.decode()

        #if token is None:
         #   raise exceptions.AuthenticationFailed('No token provided')
        auth_header = request.headers.get('Authorization')
        if not token:
            return None 
        
            # check token
            #payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])

        
        exp_timestamp = unverified_payload.get("exp")
        if not exp_timestamp:
            return HttpResponseRedirect('login/')
        else:
            print('exp_timestamp')
           
        if datetime.utcnow().timestamp() > exp_timestamp:
            return HttpResponseRedirect('login/')  # expired token
        

        try:    # check user exist
             user = SiteUser.objects.get(id=unverified_payload['user_id'])
        except SiteUser.DoesNotExist:
            print("SiteUser.DoesNotExist")
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)
