from django.shortcuts import render
from rest_framework.views import APIView
from admins.models import Activities,Food,Room
from package.models import Booking
from users.serializers import UserActivitySerializer,UserFoodSerializer,UserRoomSerializer,BookingHistorySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.



class UserActicityView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request,*args,**kwargs):

        try:
            activities = Activities.objects.all()
            serializer = UserActivitySerializer(activities,many = True)
            return Response (serializer.data,status=status.HTTP_200_OK)
        except Activities.DoesNotExist:
            return Response({"Msg":'Activities Not found'},status=status.HTTP_404_NOT_FOUND)
        


class UserFoodView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self,request,*args,**kwargs):

        try:
            foods = Food.objects.all()
            serializer = UserFoodSerializer(foods,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Food.DoesNotExist:
            return Response({"Msg":'Foods not found'},status=status.HTTP_404_NOT_FOUND)
        

class UserRoomView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self,request,*args,**kwargs):

        try:
            room = Room.objects.all()
            serializer = UserRoomSerializer(room,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"Msg":'Rooms not found'},status=status.HTTP_404_NOT_FOUND)


class BookingHistoryView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            # Assuming the Booking model has a ForeignKey to the User model named 'user'
            history = Booking.objects.filter(user=user)
            serializer = BookingHistorySerializer(history, many=True)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            return Response({"Msg": 'Not found'})