from django.db import models
from package.models import*
# Create your models here.

class Payment(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="paid_customuser")
    booking_data = models.ForeignKey(Booking,on_delete=models.CASCADE, related_name="booking_data")
    pay_amount = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'),
                                    ('Pending', 'Pending')], default='Pending')
    
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.booking_data.booking_package} - {self.payment_status}"