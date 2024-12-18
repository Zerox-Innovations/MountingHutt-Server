from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from admins.models import Blog
from admins.serializers import (
    BlogSerializer,
    CustomUserSerializer
)
from accounts.models import CustomUser
from admins.utitlities.permissions import IsAdminUser
    


class UserListAPIView(APIView):
    permission_classes = [IsAdminUser] 

    def get(self, request, user_id=None):
        if request.user.is_staff:
            if user_id:
                try:
                    user = CustomUser.objects.get(id=user_id)
                    serializer = CustomUserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except CustomUser.DoesNotExist:
                    return Response(
                    {"detail": "User not found or user is an admin."}, 
                status=status.HTTP_404_NOT_FOUND
                    )
            else:
                users = CustomUser.objects.filter(is_staff=False)
                serializer = CustomUserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"detail": "You do not have permission to access other users' profiles."}, 
            status=status.HTTP_403_FORBIDDEN
        )
      
      
      

class BlogViewset(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer