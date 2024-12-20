from django.contrib import admin
from admins.models import Blog,Food,Item_category,Activities

@admin.register(Blog)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description','created_at')

@admin.register(Item_category)
class Item_categoryAdmin(admin.ModelAdmin):
    list_display = ('id','food_time')

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description','category')



@admin.register(Activities)
class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('id','activity', 'description')
