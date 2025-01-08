from django.contrib import admin
from payment.models import Payment
# Register your models here.
@admin.register(Payment)
class PaymentgAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'booking_data', 'payment_status')