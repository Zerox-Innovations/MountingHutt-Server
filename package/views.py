from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from package.serializers import (
    PackageListSerializer,BookingRetriveSerializer,BookingSerializer,
    BookingListSerializer,BookingUpdateSerializer
)
from package.models import Package,Booking,Payment
from rest_framework import viewsets
from datetime import timedelta
import razorpay
from django.conf import settings


class PackageViewset(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)





class BookingView(APIView):

    def get(self, request, *args, **kwargs):

        package_id = request.GET.get('package_id')
        if not package_id:
            return Response({'Msg': "Enter the package_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            package_id = int(package_id)
        except (ValueError, TypeError):
            return Response({'Msg': "package_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            package = Package.objects.get(id = package_id)
            serializer = BookingRetriveSerializer(package)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Package.DoesNotExist:
            return Response({"Msg":'Package not found'},status=status.HTTP_404_NOT_FOUND)
        

    def post(self,request, *args, **kwargs):

        package_id = request.GET.get('package_id')
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
            if number_of_travelers < 4 :
                return Response({"Msg":'Should have Minimum 4 Members'})
            
            max_members = booking_package.max_members
            if max_members is not None and number_of_travelers > max_members:
                return Response({"Msg": f"The maximum number of members allowed is {max_members}"})

            
            base_price = booking_package.price
            decrement = (number_of_travelers - 4) * 200 if number_of_travelers > 4 else 0
            total_price = base_price - decrement

            payble_amount = round(total_price * 0.4)

            queryset = Booking.objects.create(

                user = request.user,
                booking_package = booking_package,
                travel_start_date = travel_start_date,
                travel_end_date  = travel_end_date,
                number_of_travelers = number_of_travelers,
                total_price = total_price,
                advance_amount = payble_amount,
                contact_number = serializer.validated_data.get('contact_number'),
                email = serializer.validated_data.get('email'),
                
            )
            response_serializer = BookingSerializer(queryset)
            response_data = {
                "total_price": queryset.total_price,
                "advance_amount": queryset.advance_amount,
                "status": queryset.status,
                "booking_date": queryset.booking_date,
                "travel_end_date":queryset.travel_end_date,
                "serializer":response_serializer.data
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingListAndUpdateView(APIView):

    def get(self,request,*args,**kwargs):
        try:
            user_bookings = Booking.objects.filter(user = request.user)
            serializer = BookingListSerializer(user_bookings,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"Msg":'You did/nt any booking till now'},status=status.HTTP_404_NOT_FOUND)
        


    def put(self,request,*args,**kwargs):

        
        booking_id = request.GET.get('booking_id')
        if not booking_id:
            return Response({'Msg': "Enter the booking_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            booking_id = int(booking_id)
        except (ValueError, TypeError):
            return Response({'Msg': "booking_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usr_bookings = Booking.objects.get(user = request.user,id=booking_id)
            serializer = BookingUpdateSerializer(usr_bookings,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Booking.DoesNotExist:
            return Response({"Msg":'Booking Not Found'})





razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)

class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        booking_id = request.GET.get('booking_id')
        
        if not booking_id:
            return Response({'Msg': "Enter the booking_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            booking_id = int(booking_id)
        except (ValueError, TypeError):
            return Response({'Msg': "booking_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            booking = Booking.objects.get(id=booking_id, user=user)
        except Booking.DoesNotExist:
            return Response({"error": "Invalid booking ID or booking does not belong to the user."}, status=400)

        # Generate Razorpay order
        amount = booking.advance_amount * 100  # Amount in paise
        currency = 'INR'
        try:
            razorpay_order = razorpay_client.order.create({
                "amount": amount,
                "currency": currency,
                "payment_capture": "1"  # Auto-capture payments
            })

            # Save order details in your database
            payment = Payment.objects.create(
                user=user,
                booking_data=booking,
                pay_amount=booking.advance_amount,
                payment_status="Pending",
                razorpay_order_id=razorpay_order["id"]
            )

            # Send order details to frontend
            return Response({
                "razorpay_order_id": razorpay_order["id"],
                "amount": amount,
                "currency": currency,
                "payment_status": "Pending"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to create Razorpay order: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

