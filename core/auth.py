from datetime import datetime
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import SiteUser
from django.http import HttpResponseRedirect
import jwt 
from rest_framework.request import HttpRequest
from rest_framework.exceptions  import AuthenticationFailed
login_attempts = {}

class JwtAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request:HttpRequest):
     
        token = request.COOKIES.get('user_token')
        
        if isinstance(token, bytes):
            token = token.decode()

        if not token:
            request.token_expired = True
            return None 
        
        try:
            unverified_payload = jwt.decode(token, options={"verify_signature": False})
            jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            request.token_expired = True
            return None

        exp_timestamp = unverified_payload.get("exp")
        if not exp_timestamp or datetime.utcnow().timestamp() > exp_timestamp:
            request.token_expired = True
            return None
        
        
        try:    # check user exist
             user = SiteUser.objects.get(id=unverified_payload['user_id'])
        except SiteUser.DoesNotExist:
            print("SiteUser.DoesNotExist")
            return None

        return (user, None)
