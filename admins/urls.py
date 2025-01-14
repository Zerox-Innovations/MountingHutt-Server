from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    BlogViewset,
    UserListAPIView,
    AdminBookingListView,AdminDashboardView,
    AdminActivityView,AdminFoodView,AdminRoomView

)


router = DefaultRouter()
router.register("blogs", BlogViewset, basename="blogs")

urlpatterns = [
    path("", include(router.urls)),
    path('users/', UserListAPIView.as_view(), name='user-list'), 
    path('users/<int:user_id>/', UserListAPIView.as_view(), name='user-profile'),  
    path('adminbookings/', AdminBookingListView.as_view(), name='adminbookings'),  
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),  
    path('activity/', AdminActivityView.as_view(), name='activity'),  
    path('foods/', AdminFoodView.as_view(), name='foods'),  
    path('rooms/', AdminRoomView.as_view(), name='rooms'),  
]
