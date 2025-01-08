from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from package.models import Booking
from payment.models import Payment
from datetime import timedelta
import razorpay
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
import uuid

# Create your views here.



razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

class PaymentView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request, *args, **kwargs):
        user = request.user
        booking_id = request.GET.get('booking_id')
        
        if not booking_id:
            return Response({'Msg': "Enter the booking_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            booking_id = uuid.UUID(booking_id)  # This ensures the booking_id is a valid UUID
        except ValueError:
            return Response({'Msg': "booking_id must be a valid UUID"}, status=status.HTTP_400_BAD_REQUEST)
        
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

    return render(request, 'razpayment.html', {
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