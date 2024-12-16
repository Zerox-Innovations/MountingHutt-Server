from django.db import models


class Package(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)   
    days = models.PositiveIntegerField(default=1)
    nights = models.PositiveIntegerField(default=1)
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
