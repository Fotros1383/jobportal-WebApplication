from datetime import datetime
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import SiteUser
from django.http import HttpResponseRedirect
import jwt 


class JwtAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:         # check header validation
            return None
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
                # check token
            #payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        
        exp_timestamp = unverified_payload.get("exp")
        if not exp_timestamp:
            return HttpResponseRedirect('login/')

        if datetime.datetime.utcnow().timestamp() > exp_timestamp:
            return HttpResponseRedirect('login/')  # expired token

  
        
        try:    # check user exist
             user = SiteUser.objects.get(id=unverified_payload['user_id'])
        except SiteUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)
