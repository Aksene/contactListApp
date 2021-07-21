from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework import response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt

# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED)
                
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        data=request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username,password=password)

        if user:
            auth_token= jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY,algorithm="HS256")
            serializer = UserSerializer(user) # if more than 1 do: many=True

            data = {'user': serializer.data, 'token': auth_token}
            return response.Response(data, status=status.HTTP_200_OK)

            # SEND RES
        return response.Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
