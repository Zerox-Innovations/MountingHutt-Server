from django.urls import path
from accounts.views import UserRegistrationAPIView,UserLoginAPIView,UserProfileAPIView

urlpatterns = [
    path('register/',UserRegistrationAPIView.as_view(),name='register'),
    path('login/',UserLoginAPIView.as_view(),name='login'),
    path('profile/',UserProfileAPIView.as_view(),name='login')
]
