from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from admins.models import Blog,Activities,Food,Room
from admins.serializers import (
    BlogSerializer,
    CustomUserSerializer,
    AdminBookingListSerializer,
    ActivitySerializer,ActivityRetriveSerializer,AdminFoodSerializer,
    AdminFoodRetriveSerializer,AdminRoomSerializer,AdminRoomRetriveSerializer
)
from accounts.models import CustomUser
from package.models import Booking,Package
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




class AdminBookingListView(APIView):
    permission_classes = [IsAdminUser] 
    def get(self,request,*args,**kwargs):

        try:
            Booking_status = request.query_params.get('status')
            

            queryset = Booking.objects.all()
            if Booking_status:
                queryset = queryset.filter(status=Booking_status)
            serializer = AdminBookingListSerializer(queryset,many =True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"Msg":'Bookings not yet'},status=status.HTTP_404_NOT_FOUND)
        



class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser] 
    def get(self,request,*args,**kwargs):

        try:
            booking_count = Booking.objects.all().count()
            user_count = CustomUser.objects.count()
            package_count = Package.objects.count()

            return Response(
                {
                    "Msg": "Dashboard statistics",
                    "data": {
                        "total_bookings": booking_count,
                        "total_users": user_count,
                        "total_packages": package_count,
                    },
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        


class AdminActivityView(APIView):
    permission_classes = [IsAdminUser] 
    def post(self,request,*args,**kwargs):

        serializer = ActivitySerializer(data= request.data)

        if serializer.is_valid():

            activity = Activities.objects.create(
                activity = serializer.validated_data.get('activity'),
                image = serializer.validated_data.get('image'),
                description = serializer.validated_data.get('description'),
                price = serializer.validated_data.get('price'),

            )
            
            if activity.image:
                activity.image = request.build_absolute_uri(activity.image.url)
            response_serializer = ActivitySerializer(activity)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def get(self,request,*args,**kwargs):
        
        try:
            queryset = Activities.objects.all()
            serializer = ActivityRetriveSerializer(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Activities.DoesNotExist:
            return Response({"Msg":'Activities Create yet'},status=status.HTTP_404_NOT_FOUND)
        

    def put(self,request,*args,**kwargs):


        activity_id = request.GET.get('activity_id')
        if not activity_id:
            return Response({'Msg': "Enter the activity_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            activity_id = int(activity_id)
        except (ValueError, TypeError):
            return Response({'Msg': "activity_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = Activities.objects.get(id = activity_id)
            serializer = ActivitySerializer(queryset,data=request.data,partial = True)
            if serializer.is_valid():
                
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        


    def delete(self,request,*args,**kwargs):
        

        activity_id = request.GET.get('activity_id')
        if not activity_id:
            return Response({'Msg': "Enter the activity_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            activity_id = int(activity_id)
        except (ValueError, TypeError):
            return Response({'Msg': "activity_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            queryset = Activities.objects.get(id = activity_id)
            queryset.delete()
            return Response({"Msg":f'Delete Activity {queryset.activity}'},status=status.HTTP_200_OK)
        except Activities.DoesNotExist:
            return Response({"Msg":'Sctivity Not Found'},status=status.HTTP_404_NOT_FOUND)

                

class AdminFoodView(APIView):
    permission_classes = [IsAdminUser] 
    def post(self,request,*args,**kwargs):

        serializer = AdminFoodSerializer(data = request.data)

        if serializer.is_valid():


            food = Food.objects.create(

                item = serializer.validated_data.get('item'),
                image = serializer.validated_data.get('image'),
                description = serializer.validated_data.get('description'),
                time = serializer.validated_data.get('time'),
                category = serializer.validated_data.get('category'),
                price = serializer.validated_data.get('price'),
                
            )
            if food.image:
                food.image = request.build_absolute_uri(food.image.url)
            response_serializer = AdminFoodSerializer(food)
            return Response(response_serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    



    def get(self,request,*args,**kwargs):

        try:
            food = Food.objects.all()
            serializer = AdminFoodRetriveSerializer(food,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Food.DoesNotExist:
            return Response({"Msg":'Foods not add yet'},status=status.HTTP_404_NOT_FOUND)
        

    def put(self,request,*args,**kwargs):

        food_id = request.GET.get('food_id')
        if not food_id:
            return Response({'Msg': "Enter the food_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            food_id = int(food_id)
        except (ValueError, TypeError):
            return Response({'Msg': "food_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            food = Food.objects.get(id=food_id)
            serializer = AdminFoodSerializer(food,data=request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Food.DoesNotExist:
            return Response({"Msg":'Food not found'},status=status.HTTP_404_NOT_FOUND)
        

    def delete(self,request,*args,**kwargs):


        food_id = request.GET.get('food_id')
        if not food_id:
            return Response({'Msg': "Enter the food_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            food_id = int(food_id)
        except (ValueError, TypeError):
            return Response({'Msg': "food_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            food = Food.objects.get(id=food_id)
            food.delete()
            return Response({"Msg":f'Deleted food item: {food}'},status=status.HTTP_200_OK)
        except Food.DoesNotExist:
            return Response




class AdminRoomView(APIView):
    permission_classes = [IsAdminUser] 
    def post(self,request,*arg,**kwargs):

        serializer = AdminRoomSerializer(data = request.data)
        if serializer.is_valid():

            room = Room.objects.create(

                room_name = serializer.validated_data.get('room_name'),
                image = serializer.validated_data.get('image'),
                capacity = serializer.validated_data.get('capacity'),
                description = serializer.validated_data.get('description'),
                price = serializer.validated_data.get('price'),

            )
            if room.image:
                room.image = request.build_absolute_uri(room.image.url)
            response_serializer = AdminRoomSerializer(room)
            return Response(response_serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def get(self,request,*args,**kwargs):

        try:
            room = Room.objects.all()
            serializer = AdminRoomRetriveSerializer(room,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"Msg":'Room Not found'},status=status.HTTP_404_NOT_FOUND)
        


    def put(self,request,*args,**kwargs):


        room_id = request.GET.get('room_id')
        if not room_id:
            return Response({'Msg': "Enter the room_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            room_id = int(room_id)
        except (ValueError, TypeError):
            return Response({'Msg': "room_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room = Room.objects.get(id=room_id)
            serializer = AdminRoomSerializer(room,data=request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Room.DoesNotExist:
            return Response({"Msg":'Food not found'},status=status.HTTP_404_NOT_FOUND)



    def delete(self,request,*args,**kwargs):


        room_id = request.GET.get('room_id')
        if not room_id:
            return Response({'Msg': "Enter the room_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            room_id = int(room_id)
        except (ValueError, TypeError):
            return Response({'Msg': "room_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room = Room.objects.get(id=room_id)
            room.delete()
            return Response({"Msg":f'Deleted room: {room}'},status=status.HTTP_200_OK)
        except Food.DoesNotExist:
            return Response

        


