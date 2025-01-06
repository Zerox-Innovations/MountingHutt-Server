from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from accounts.serializers import (
    UserSerializer, 
    UserLoginSerializer , 
    UserProfileSerializer,
    UserProfileUpdateSerializer
)
from django.contrib.auth import authenticate
from accounts.utils.token import get_tokens_for_user
from accounts.models import CustomUser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
  
class UserRegistrationAPIView(APIView):
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'message': 'User registered successfully', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        # If the request is not valid, return a bad request response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      
class UserLoginAPIView(APIView):
  
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({
                    "msg":"User Loggined successfully",
                    "token":token
                },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = CustomUser.objects.get(id=request.user.id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self,request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

