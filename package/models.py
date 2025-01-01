from django.db import models
from accounts.models import CustomUser

class Package(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    banner_image = models.ImageField(null=True,blank=True)   
    days = models.PositiveIntegerField(default=1)
    nights = models.PositiveIntegerField(default=1)
    max_members = models.PositiveIntegerField(null=True,blank=True)
    price = models.PositiveIntegerField()
    additional_info = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
      

class DayDetail(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='day_details')
    day_number = models.CharField(max_length=10)
    description = models.TextField()  

    def __str__(self):
        return f"Day {self.day_number} - {self.package.title}"



class Booking(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="customuser")
    booking_package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="package")
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_start_date = models.DateField()
    travel_end_date = models.DateField()
    number_of_travelers = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()
    advance_amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('Confirmed', 'Confirmed'),('Pending', 'Pending'), 
                                                      ('Cancelled', 'Cancelled')],default='Pending')
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    razorpay_order_id = models.CharField(null=True,blank=True)

    def __str__(self):
        return f"{self.user} - {self.booking_package.title} - {self.status}"
    


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
    