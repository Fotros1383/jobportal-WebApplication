from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,CurrentUserSerializer
from django.contrib.auth import authenticate
from .utils import genetate_jwt
from rest_framework.permissions import IsAuthenticated
from datetime import timezone, timedelta, datetime
from rest_framework.request import Request
from .models import Resume

EXPIRE_MINUTE_LOGIN = 10
EXPIRE_MINUTE_COOKIES = 5

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)   # can send a message as a json
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token = genetate_jwt(user,EXPIRE_MINUTE_LOGIN)
        # set cookies
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTE_COOKIES)   
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(
            key='user_token',
            value=token,
            expires=expire_time
        )
        
        return response  # can send a message for fronend
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_resume(request:Request):
    if request.user.role != 'JOB_SEEKER':
        return Response(status=status.HTTP_403_FORBIDDEN)
    if 'resume' not in request.FILES:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    resume = Resume.objects.create(
        user=request.user,
        file=request.FILES['resume']
    )
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_resumes(request:Request):
    if request.user.role != 'EMPLOYER':
        return Response(status=status.HTTP_403_FORBIDDEN)
    resumes = Resume.objects.all()
    data = [
        {
            'user': resume.user.username,
            'file': resume.file.url,
            # 'file': request.build_absolute_uri(resume.file.url),
            'uploaded at': resume.uploaded_at
        }
        for resume in resumes
    ]
    return Response(data=data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    response = Response(status=status.HTTP_200_OK)  # can send a message as a json
    response.delete_cookie('user_token')
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request:Request):
    serializer = CurrentUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

