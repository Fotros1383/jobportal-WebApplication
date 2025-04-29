import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from .models import SiteUser

def genetate_jwt(user:SiteUser, expire_minutes=5):
    payload = {
        "user_id" : user.id,
        "username" : user.username,    # for more information -> we use it in front
        "role" : user.role,
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    }
    token = jwt.encode(payload=payload,
                       key=settings.SECRET_KEY,
                        algorithm='HS256'
                       )
    return token
