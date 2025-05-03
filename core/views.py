from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,CurrentUserSerializer
from django.contrib.auth import authenticate
from .utils import genetate_jwt
from rest_framework.permissions import IsAuthenticated
from datetime import timezone, timedelta, datetime
from rest_framework.permissions import AllowAny
from django.http import HttpRequest,HttpResponse

EXPIRE_MINUTE_LOGIN = 10
EXPIRE_MINUTE_COOKIES = 5

@api_view(['POST','GET'])
@permission_classes([AllowAny]) 
def register(request:HttpRequest):
    if(request.method=='GET'):
        return HttpResponse('you are in register page')
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)   # can send a message as a json
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST','GET'])
@permission_classes([AllowAny]) 
def login(request):
    if(request.method=='GET'):
        return HttpResponse('you are in login page')
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token = genetate_jwt(user,EXPIRE_MINUTE_LOGIN)
        # set cookies
        expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTE_COOKIES)   
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            key='user_token',
            value=token,
            expires=expire
        )
        
        return response  # can send a message for fronend
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    if(request.method=='GET'):
        return HttpResponse('you are in logout page, sad to see you go')
    response = Response(status=status.HTTP_200_OK)  # can send a message as a json
    response.delete_cookie('user_token')
    return response

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    if(request.method=='GET'):
        return HttpResponse('you are in profile page')
    serializer = CurrentUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

