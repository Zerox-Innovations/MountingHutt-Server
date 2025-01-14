from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from package.serializers import (
    PackageListSerializer,PackageRetriveForBookingSerializer,BookingSerializer,
    BookingCheckoutSerializer,BookingListSerializer,BookingUpdateSerializer,PackgeImageSerializer,
    PackgeImageListSerializer,PackgeImageGetUpdateSerializer
)
from package.models import Package,Booking,PackageImage
from rest_framework import viewsets
from datetime import timedelta
import razorpay
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
import uuid


class PackageViewset(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class PackageImageView(APIView):

    def post(self,request,*args,**kwargs):
        package_id = request.GET.get('package_id')
        if not package_id:
            return Response({'Msg': "Enter the package_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            package_id = int(package_id)
        except (ValueError, TypeError):
            return Response({'Msg': "package_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            package = Package.objects.get(id = package_id)
            pass
        except Package.DoesNotExist:
            return Response({"Msg":'Package noy found'})
        serializer = PackgeImageSerializer(data=request.data, context={'package': package})

        if serializer.is_valid():
            # Save the image and package
            serializer.save(package=package)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self,request,*args,**keargs):

        try:
            image = PackageImage.objects.all()
            serializer= PackgeImageListSerializer(image,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Package.DoesNotExist:
            return Response({"Msg":'Packges not found'},status=status.HTTP_404_NOT_FOUND)



class PackgeImageRetriveUpdateView(APIView):

    def get(self,request,*args,**keargs):

        image_id = request.GET.get('image_id')
        if not image_id:
            return Response({'Msg': "Enter the image_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            image_id = int(image_id)
        except (ValueError, TypeError):
            return Response({'Msg': "image_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            image = PackageImage.objects.get(id = image_id)
            serializer = PackgeImageGetUpdateSerializer(image)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except PackageImage.DoesNotExist:
            return Response({"Msg":'Package image not found'},status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,*args,**keargs):

        image_id = request.GET.get('image_id')
        if not image_id:
            return Response({'Msg': "Enter the image_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            image_id = int(image_id)
        except (ValueError, TypeError):
            return Response({'Msg': "image_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            image = PackageImage.objects.get(id = image_id)
            serializer = PackgeImageGetUpdateSerializer(image,data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except PackageImage.DoesNotExist:
            return Response({"Msg":'Packge image not found'})
        




class BookingView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs):

        package_id = request.GET.get('package_id')
        print(package_id)
        if not package_id:
            return Response({'Msg': "Enter the package_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            package_id = int(package_id)
        except (ValueError, TypeError):
            return Response({'Msg': "package_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            package = Package.objects.get(id = package_id)
            serializer = PackageRetriveForBookingSerializer(package)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Package.DoesNotExist:
            return Response({"Msg":'Package not found'},status=status.HTTP_404_NOT_FOUND)
        

    def post(self,request, *args, **kwargs):

        package_id = request.data.get('package_id')
        if not package_id:
            return Response({'Msg': "Enter the package_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            package_id = int(package_id)
        except (ValueError, TypeError):
            return Response({'Msg': "package_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        booking_package = Package.objects.get(id = package_id)
        
        serializer = BookingSerializer(data = request.data)
        if serializer.is_valid():
            travel_start_date = serializer.validated_data.get('travel_start_date')
            total_days = booking_package.nights
            travel_end_date = travel_start_date + timedelta(days=total_days)


            number_of_travelers = serializer.validated_data.get('number_of_travelers')
            
            max_members = booking_package.max_members
            if max_members is not None and number_of_travelers > max_members:
                return Response({"Msg": f"The maximum number of members allowed is {max_members}"})

            
            base_price = booking_package.price
            total_amount = base_price * number_of_travelers
            decrement = (number_of_travelers) * 200 if number_of_travelers > 4 else 0
            payable_amount = total_amount - decrement
            
            advance_amount = round(payable_amount * 0.4)
            balance_amount = payable_amount - advance_amount

            queryset = Booking.objects.create(
                id=uuid.uuid4(),
                user = request.user,
                booking_package = booking_package,
                travel_start_date = travel_start_date,
                travel_end_date  = travel_end_date,
                number_of_travelers = number_of_travelers,
                total_amount = total_amount,
                payable_amount = payable_amount,
                advance_amount = advance_amount,
                balance_amount = balance_amount,
                
            )
            response_serializer = BookingSerializer(queryset)
            response_data = {
                "total_price": queryset.total_amount,
                "payble_amount": queryset.payable_amount,
                "advance_amount": queryset.advance_amount,
                "balance_amount": queryset.balance_amount,
                "status": queryset.status,
                "booking_date": queryset.created_at,
                "travel_end_date":queryset.travel_end_date,
                "serializer":response_serializer.data
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self,request,booking_id=None, *args,**kwargs):

        booking_id = request.GET.get('booking_id')
        if not booking_id:
            return Response({'Msg': "Enter the booking_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            booking_id = uuid.UUID(booking_id)  # This ensures the booking_id is a valid UUID
        except ValueError:
            return Response({'Msg': "booking_id must be a valid UUID"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_booking = Booking.objects.get(user = request.user,id=booking_id)
            serializer = BookingCheckoutSerializer(user_booking)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"Msg":'Booking not found'},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,*args,**kwargs):

        booking_id = request.GET.get('booking_id')
        if not booking_id:
            return Response({'Msg': "Enter the booking_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            booking_id = uuid.UUID(booking_id)  # This ensures the booking_id is a valid UUID
        except ValueError:
            return Response({'Msg': "booking_id must be a valid UUID"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_booking = Booking.objects.get(user = request.user,id=booking_id)
            serializer = BookingCheckoutSerializer(user_booking,data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Booking.DoesNotExist:
            return Response({"Msg":'User Booking not found'},status=status.HTTP_404_NOT_FOUND)




class BookingGetAndUpdateView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self,request,*args,**kwargs):
        
            booking_id = request.GET.get('booking_id')
            if not booking_id:
                user_bookings = Booking.objects.filter(user=request.user)
            
                if not user_bookings.exists():  # Check if there are no bookings for the user
                    return Response({'Msg': "No bookings found for this user"}, status=status.HTTP_404_NOT_FOUND)
                
                serializer = BookingListSerializer(user_bookings, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            try:
                booking_id = uuid.UUID(booking_id)  # This ensures the booking_id is a valid UUID
            except ValueError:
                return Response({'Msg': "booking_id must be a valid UUID"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user_booking = Booking.objects.get(user = request.user,id=booking_id)
                serializer = BookingListSerializer(user_booking)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Booking.DoesNotExist:
                return Response({"Msg":'Booking not found'},status=status.HTTP_404_NOT_FOUND)
        


    def put(self,request,*args,**kwargs):

        
        booking_id = request.GET.get('booking_id')
        if not booking_id:
            return Response({'Msg': "Enter the booking_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            booking_id = uuid.UUID(booking_id)  # This ensures the booking_id is a valid UUID
        except ValueError:
            return Response({'Msg': "booking_id must be a valid UUID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usr_booking = Booking.objects.get(user = request.user,id=booking_id)
            serializer = BookingUpdateSerializer(usr_booking,data=request.data,partial=True)
            if serializer.is_valid():
                
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Booking.DoesNotExist:
            return Response({"Msg":'Booking Not Found'})



