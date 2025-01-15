from django.db import models
from accounts.models import CustomUser
import uuid
from cloudinary.models import CloudinaryField


class Package(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500) 
    banner_image = CloudinaryField(null=True,blank=True)
    background_image = CloudinaryField(null=True,blank=True)
    days = models.PositiveIntegerField(default=1)
    nights = models.PositiveIntegerField(default=1)
    min_members = models.PositiveBigIntegerField(null=True,blank=True)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="customuser")
    booking_package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="package")
    created_at = models.DateTimeField(auto_now_add=True)
    travel_start_date = models.DateField()
    travel_end_date = models.DateField()
    number_of_travelers = models.PositiveIntegerField(default=1)
    total_amount = models.PositiveIntegerField()
    payable_amount = models.PositiveIntegerField(null=True,blank=True)
    advance_amount = models.PositiveIntegerField()
    balance_amount = models.PositiveIntegerField(null=True,blank=True)
    status = models.CharField(max_length=20, choices=[('Confirmed', 'Confirmed'),('Pending', 'Pending'), 
                                                      ('Cancelled', 'Cancelled')],default='Pending')
    first_name = models.CharField(max_length=250,null=True,blank=True)
    last_name = models.CharField(max_length=250,null=True,blank=True)
    zip_code = models.CharField(max_length=15,null=True,blank=True)
    pro_noun = models.CharField(max_length=20, choices=[('Mr', 'Mr'),('Mrs', 'mrs')],null=True,blank=True)
    contact_number = models.CharField(max_length=15,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    


    def __str__(self):
        return f"{self.user} - {self.booking_package.title} - {self.status}"
    
