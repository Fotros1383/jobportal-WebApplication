from django.http import HttpResponse, HttpResponseRedirect
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
from rest_framework.exceptions import AuthenticationFailed


EXPIRE_MINUTE_COOKIES = 5
EXPIRE_DAY_REMEMBER_ME = 7
EXPIRE_MINUTE_BRUTEFORCE = 5
MAXIMUM_TRY = 5

@api_view(['POST','GET'])
@permission_classes([AllowAny]) 
def register(request:Request):
    if(request.method=='GET'):
       return render(request,'./register-page new c.html',status=status.HTTP_200_OK)
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'You registered successfully!'},status=status.HTTP_201_CREATED)   # can send a message as a json
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST','GET'])
@permission_classes([AllowAny]) 
def login(request):
    try:
        if(request.method=='GET'):
           return render(request,'./login-page new c.html',status=status.HTTP_200_OK)
        username = request.data.get('username')
        password = request.data.get('password')
        remember_me = request.data.get('remember_me', False)
        user_attempt = login_attempts.get(username)

        if user_attempt and 'blocked_until' in login_attempts[username]:
            if datetime.now(timezone.utc) < user_attempt['blocked_until']:
                 return Response({'error':'Too many Try to login. Try again later'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
        user = authenticate(username=username, password=password)
    
        if user:
            if username in login_attempts:
                del login_attempts[username]
        
            token = genetate_jwt(user,EXPIRE_MINUTE_COOKIES)
            # set cookies
            expire_time = timedelta(days=EXPIRE_DAY_REMEMBER_ME) if remember_me else timedelta(minutes=EXPIRE_MINUTE_COOKIES)
            response = Response({'message': 'Login successfull'},status=status.HTTP_200_OK)
            response.set_cookie(
                key='user_token',
                value=token,
                expires=expire_time+datetime.now(timezone.utc)
            )
           
        
            return response
        
        if not user_attempt:
            login_attempts[username] = {'count': 1, 'last_attempt': datetime.now(timezone.utc)}
        else:
            login_attempts[username]['count'] += 1
            login_attempts[username]['last_attemps'] = datetime.now(timezone.utc)
            
            if login_attempts[username]['count'] >= MAXIMUM_TRY:
                login_attempts[username]['blocked_until'] = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTE_BRUTEFORCE)        
        return Response({'error':'Invalid username or password'},status=status.HTTP_401_UNAUTHORIZED)
    except AuthenticationFailed:
            return HttpResponseRedirect('api/login/').delete_cookie('user_token')
    
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def upload_resume(request:Request):
    if request.user.role != 'JOB_SEEKER':
        return Response(status=status.HTTP_403_FORBIDDEN)
    if 'resume' not in request.FILES:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    Resume.objects.create(
        user=request.user,
        file=request.FILES['resume']
    )
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_resumes(request:Request):
    if request.user.role not in ['EMPLOYER', 'JOB_SEEKER']:
        return Response(status=status.HTTP_403_FORBIDDEN)
        
    if request.user.role == 'EMPLOYER':
        resumes = Resume.objects.all()
    else:
        resumes = Resume.objects.filter(user=request.user)
        
    data = [
        {
            'user': resume.user.username,
            'user_name': resume.user.first_name + ' ' + resume.user.last_name,
            'file': resume.file.url,
            'uploaded_at': resume.uploaded_at
        }
        for resume in resumes
    ]
    return render(request, './resumes-page.html', {
        'resumes': data,
        'status': 200
    })




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    response=render(request,template_name='./logout-page.html',status=200)
    response.delete_cookie('user_token')
    return response

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def profile(request):

    if(request.method=='GET'):
        return render(request,'./profile-page.html',status=200)
    
    serializer = CurrentUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_resume(request: Request):
    if request.user.role != 'JOB_SEEKER':
        return Response(status=status.HTTP_403_FORBIDDEN)
        
    if 'resume' not in request.FILES:
        return Response(
            {'error': 'No resume file provided'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
        
    Resume.objects.create(
        user=request.user,
        file=request.FILES['resume']
    )
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def root_page(request:Request):
    return render(request,template_name='./root-page.html',status=200)
