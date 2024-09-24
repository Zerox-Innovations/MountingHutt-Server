from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializers import UserSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from accounts.utils.token import get_tokens_for_user

  
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
                    "token":token},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)