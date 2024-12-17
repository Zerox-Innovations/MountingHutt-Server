from django.db import models

# Create your models here.


class Blog(models.Model):
    image = models.ImageField(upload_to='blogs',blank=True,null=True)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=250,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title
    