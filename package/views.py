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





class BookingView(APIView):
    permission_classes = [IsAuthenticated] 
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
            # if number_of_travelers < min_members :
            #     return Response({"Msg":f'Should have Minimum {min_members} members'})
            
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
                first_name = serializer.validated_data.get('first_name'),
                last_name = serializer.validated_data.get('last_name'),
                zip_code = serializer.validated_data.get('zip_code'),
                pro_noun = serializer.validated_data.get('pro_noun'),
                contact_number = serializer.validated_data.get('contact_number'),
                email = serializer.validated_data.get('email'),
                
            )
            response_serializer = BookingSerializer(queryset)
            response_data = {
                "total_price": queryset.total_amount,
                "payble_amount": queryset.payable_amount,
                "advance_amount": queryset.advance_amount,
                "balance_amount": queryset.balance_amount,
                "status": queryset.status,
                "booking_date": queryset.booking_date,
                "travel_end_date":queryset.travel_end_date,
                "serializer":response_serializer.data
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingListAndUpdateView(APIView):
    permission_classes = [IsAuthenticated] 
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





razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

class PaymentView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def post(self, request, *args, **kwargs):
        user = request.user
        booking_id = kwargs.get('booking_id')
        
        if not booking_id:
            return Response({'Msg': "Enter the booking_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            booking_id = int(booking_id)
        except (ValueError, TypeError):
            return Response({'Msg': "booking_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            booking = Booking.objects.get(id=booking_id, user=user)
        except Booking.DoesNotExist:
            return Response({"error": "Invalid booking ID or booking does not belong to the user."}, status=status.HTTP_404_NOT_FOUND)

       
        if not booking.advance_amount or booking.advance_amount <= 0:
            return Response({"error": "Invalid advance amount for booking."}, status=status.HTTP_400_BAD_REQUEST)

        
        amount = booking.advance_amount * 100  # Amount in paise
        currency = 'INR'
        payment_description = f"Booking ID: {booking_id} - Advance Payment"

        try:
            # Razorpay Payment Link creation
            payment_link = razorpay_client.payment_link.create({
                "amount": amount,
                "currency": currency,
                "description": payment_description,
                "notify": {
                    "email": True,  
                    "sms": True      
                },
                "customer": {
                    "name": user.name, 
                    "email": user.email
                },
                "reminder_enable": True ,
                "callback_url": "http://127.0.0.1:8000/payment-success/",  # Replace with your actual domain and success URL
                "callback_method": "get"  # or "post"
            })

            
            payment = Payment.objects.create(
                user=user,
                booking_data=booking,
                pay_amount=booking.advance_amount,
                payment_status="Pending",
                razorpay_payment_id=payment_link['id']
            )
            
           
            return Response({
                "payment_link": payment_link['short_url'], 
                "amount": amount,
                "currency": currency,
                "payment_status": payment.payment_status
            }, status=status.HTTP_201_CREATED)

        except razorpay.errors.BadRequestError as e:
            return Response({"error": f"Razorpay Bad Request: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except razorpay.errors.ServerError as e:
            return Response({"error": f"Razorpay Server Error: {str(e)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": f"Failed to create Razorpay payment link: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from django.shortcuts import render
from django.http import HttpResponse

def payment_success_view(request):
    payment_id = request.GET.get('razorpay_payment_id', None)
    status = request.GET.get('status', None)

    if not payment_id or status != "captured":
        return HttpResponse("Payment unsuccessful. Please try again.", status=400)

    # Optional: Verify the payment details using Razorpay's API if required
    # payment_details = razorpay_client.payment.fetch(payment_id)

    return render(request, 'payment.html', {
        "payment_id": payment_id,
        "status": status
    })



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
@csrf_exempt
def razorpay_webhook(request):
    if request.method == "POST":
        payload = request.body
        signature = request.headers.get('X-Razorpay-Signature')
        
        try:
            razorpay_client.utility.verify_webhook_signature(payload, signature, 'your_webhook_secret')
            event = json.loads(payload)

            if event['event'] == 'payment.captured':
                payment_id = event['payload']['payment']['entity']['id']
                # Update your payment record in the database
                payment = Payment.objects.filter(razorpay_payment_id=payment_id).first()
                if payment:
                    payment.payment_status = "Success"
                    payment.save()
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"error": "Invalid signature"}, status=400)

    return JsonResponse({"status": "ok"})
