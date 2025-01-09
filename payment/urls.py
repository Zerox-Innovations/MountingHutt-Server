from rest_framework.routers import DefaultRouter
from django.urls import path, include
from payment.views import (
    PaymentView,PaymentSuccessView,razorpay_webhook
)





urlpatterns = [
    path('payment-success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment-create/',PaymentView.as_view(),name='payment_create'),
    # path('payment-success/', payment_success_view, name='payment_success'),
    path('razorpay-webhook/', razorpay_webhook, name='razorpay_webhook'),
]