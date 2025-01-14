from django.shortcuts import render
from rest_framework.views import APIView
from admins.models import Activities,Food,Room
from package.models import Booking
from users.serializers import UserActivitySerializer,UserFoodSerializer,UserRoomSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
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



from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from users.form import ContactForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class ContactUsView(APIView):
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f"Client Message from {email}"
            body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            try:
                send_mail(
                    subject,
                    body,
                    email,  # From email
                    [settings.EMAIL_HOST_USER],  # To email
                    fail_silently=False,
                )
                return Response({'Msg': 'Email sent successfully!'}, status=200)
            except Exception as e:
                return Response({'Msg': f'Failed to send email: {str(e)}'}, status=500)
        return Response({'Msg': 'Invalid form data'}, status=400)


