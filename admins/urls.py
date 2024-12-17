from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    BlogViewset,
    UserListAPIView
)


router = DefaultRouter()
router.register("blog", BlogViewset, basename="blogs")

urlpatterns = [
    path("", include(router.urls)),
    path('users/', UserListAPIView.as_view(), name='user-list'), 
    path('users/<int:user_id>/', UserListAPIView.as_view(), name='user-profile'),  
]
