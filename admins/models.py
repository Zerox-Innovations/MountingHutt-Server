from django.db import models

# Create your models here.


class Blog(models.Model):
    image = models.ImageField(upload_to='blogs',blank=True,null=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title
    


class Activities(models.Model):

    activity = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media',blank=True,null=True)
    description = models.TextField(max_length=250,blank=True,null=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.activity




class Item_category(models.Model):
    food_time = models.CharField(max_length=250,choices=[('Breakfast','Breakfast'),('Lunch','Lunch'),
                                                         ('Dinner','Dinner')])

    def __str__(self):
        return self.food_time




class Food(models.Model):

    item = models.CharField(max_length=250,null=True,blank=True)
    image = models.ImageField(upload_to='media',blank=True,null=True)
    description = models.TextField(max_length=250,blank=True,null=True)
    time = models.ForeignKey(Item_category,on_delete=models.CASCADE,related_name='foodtime',blank=True,null=True)
    category = models.CharField(max_length=20,choices=[('Veg','Veg'),('Non-Veg','Non-Veg'),
                                                       ('Hot','Hot'),('Cool','Cool')],null=True,blank=True)
    price = models.PositiveIntegerField(null=True,blank=True)
    

    def __str__(self):
        return self.item

    
class Room(models.Model):

    room_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='media',null=True,blank=True)
    capacity = models.PositiveIntegerField()
    description = models.TextField(max_length=250)
    price = models.PositiveIntegerField()


    def __str__(self):
        return self.room_name


# class services(models.Model):

