from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import RegisterSerializer,CurrentUserSerializer
from django.contrib.auth import authenticate
from .utils import genetate_jwt
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import timezone, timedelta, datetime
from .models import Resume
from .auth import login_attempts

EXPIRE_MINUTE_LOGIN = 10
EXPIRE_MINUTE_COOKIES = 5
EXPIRE_DAY_REMEMBER_ME = 7
EXPIRE_MINUTE_BRUTEFORCE = 5

@api_view(['POST','GET'])
@permission_classes([AllowAny]) 
def register(request:Request):
    if(request.method=='GET'):
       return render(request,'./register-page new c.html',status=200)
       return render(request,'./new register.html',status=200)
      #return render(request,'./register-page.html',status=200)
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'You registered successfully!'},status=status.HTTP_201_CREATED)   # can send a message as a json
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST','GET'])
@permission_classes([AllowAny]) 
def login(request):
    if(request.method=='GET'):
        return render(request,'./login-page new c.html',status=status.HTTP_200_OK)
         #return render(request,'./login-page.html',status=status.HTTP_200_OK)
        #return HttpResponse('you are in login-page page',status=status.HTTP_200_OK)
    username = request.data.get('username')
    password = request.data.get('password')
    remember_me = request.data.get('remember_me', False)
    user_attempt = login_attempts.get(username)

    if user_attempt and 'blocked_until' in login_attempts:
        if datetime.now(timezone.utc) < user_attempt['blocked_until']:
            return Response({'error':'Too many request to login. Try again later'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    user = authenticate(username=username, password=password)
    
    if user:
        token = genetate_jwt(user,EXPIRE_MINUTE_LOGIN)
        # set cookies
        expire_time = timedelta(days=EXPIRE_DAY_REMEMBER_ME) if remember_me else timedelta(minutes=EXPIRE_MINUTE_COOKIES)
        response = Response({'message': 'Login successfull'},status=status.HTTP_200_OK)
        response.set_cookie(
            key='user_token',
            value=token,
            expires=expire_time+datetime.now(timezone.utc)
        )
        response.headers
    
        return response
    
    if not user_attempt:
        login_attempts[username] = {'count': 1, 'last_attempt': datetime.now(timezone.utc)}
    else:
        login_attempts[username]['count'] += 1
        login_attempts[username]['last_attemps'] = datetime.now(timezone.utc)
        
        if login_attempts[username]['count'] >= 5:
            login_attempts[username]['blocked_until'] = datetime.now(timezone.utc) + timedelta(minute=EXPIRE_MINUTE_BRUTEFORCE)
    
    return Response({'error':'Invalid username or password'},status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST','GET'])
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    response=render(request,template_name='./logout-page.html',status=200)
    response.delete_cookie('user_token')
        #return Response({'message': 'you are in logout page, sad to see you go'},status=status.HTTP_200_OK)
    #response = HttpResponseResponse({'message': 'Logout succeessfull'},status=status.HTTP_200_OK)  # can send a message as a json
    #response.delete_cookie('user_token')
    return response

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    if(request.method=='GET'):
        return render(request,'./profile-page.html',status=200)
        return HttpResponse('you are in profile page',status=status.HTTP_200_OK)
    
    serializer = CurrentUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

