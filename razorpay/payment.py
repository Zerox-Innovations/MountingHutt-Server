from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from package.models import Booking,Payment
import razorpay

from django.http import JsonResponse

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        try:
            data = request.POST
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")

            # Verify payment signature
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }

            try:
                razorpay_client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({"error": "Invalid payment signature"}, status=400)

            # Update payment record in the database
            Payment.objects.filter(razorpay_order_id=razorpay_order_id).update(
                payment_status="Paid",
                razorpay_payment_id=razorpay_payment_id
            )

            return JsonResponse({"message": "Payment verified successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Verification failed: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)




def capture_payment(payment_id, amount):
    try:
        razorpay_client.payment.capture(payment_id, amount)
        return True
    except Exception as e:
        return False
# authorize razorpay client with API Keys.
# razorpay_client = razorpay.Client(
#     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# def homepage(request):
#     currency = 'INR'
#     amount = 20000  # Rs. 200

#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))

#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'

#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url

#     return render(request, 'index.html', context=context)


# # we need to csrf_exempt this url as
# # POST request will be made by Razorpay
# # and it won't have the csrf token.
# @csrf_exempt
# def paymenthandler(request):

#     # only accept POST request.
#     if request.method == "POST":
#         try:
          
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }

#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(
#                 params_dict)
#             if result is not None:
#                 amount =   # Rs. 200
#                 try:

#                     # capture the payemt
#                     payment = razorpay_client.payment.capture(payment_id,  request.POST.get('amount', 0))

#                     # render success page on successful caputre of payment
#                     return render(request, 'paymentsuccess.html')
#                 except:

#                     # if there is an error while capturing payment.
#                     return render(request, 'paymentfail.html')
#             else:

#                 # if signature verification fails.
#                 return render(request, 'paymentfail.html')
#         except:

#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#        # if other than POST request is made.
#         return HttpResponseBadRequest()