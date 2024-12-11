from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from package.serializers import (
    PackageListSerializer
)
from package.models import Package
from rest_framework import viewsets



class PackageViewset(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer
      
    def retrieve(self, request, *args, **kwargs):
        package = self.get_object()
        serializer = self.get_serializer(package)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class PackageDetailViewset(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer
      
    def list(self, request, *args, **kwargs):
        packages = self.queryset
        serializer = self.get_serializer(packages,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def perform_create(self, serializer):
        serializer.save()