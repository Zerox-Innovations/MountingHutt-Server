
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from package.views import (
    PackageViewset,
    BookingView,BookingListAndUpdateView,PaymentView,payment_success_view,razorpay_webhook
)


router = DefaultRouter()
router.register("packages", PackageViewset, basename="package")
# router.register("packageDetail", PackageDetailViewset, basename="packageDetail")


urlpatterns = [
    path("", include(router.urls)),
    path('booking/',BookingView.as_view(),name='booking'),
    path('bookings/',BookingListAndUpdateView.as_view(),name='bookings'),
    path('payment/',PaymentView.as_view(),name='payment'),
    path('payment-success/', payment_success_view, name='payment_success'),
    path('razorpay-webhook/', razorpay_webhook, name='razorpay_webhook'),
]
