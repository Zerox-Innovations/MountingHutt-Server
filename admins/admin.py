from django.contrib import admin
from admins.models import Blog

@admin.register(Blog)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description','created_at')
