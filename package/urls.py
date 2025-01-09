
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from package.views import (
    PackageViewset,
    BookingView,CheckoutView,BookingGetAndUpdateView,PackageImageView,PackgeImageRetriveUpdateView
)


router = DefaultRouter()
router.register("packages", PackageViewset, basename="package")
# router.register("packageDetail", PackageDetailViewset, basename="packageDetail")


urlpatterns = [
    path("", include(router.urls)),
    path('booking/',BookingView.as_view(),name='booking'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('bookings/',BookingGetAndUpdateView.as_view(),name='bookings'),
    path('image/',PackageImageView.as_view(),name='image'),
    path('image-update/',PackgeImageRetriveUpdateView.as_view(),name='update'),

]
