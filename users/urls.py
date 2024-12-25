from rest_framework.routers import DefaultRouter
from django.urls import path, include
from users.views import UserActicityView,UserFoodView,UserRoomView



urlpatterns = [
    path('useractivity/',UserActicityView.as_view(),name='useractivity'),
    path('userfood/',UserFoodView.as_view(),name='userfood'),
    path('user_room/',UserRoomView.as_view(),name='user_room'),
   
]
