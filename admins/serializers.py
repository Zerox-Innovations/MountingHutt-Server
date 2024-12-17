from rest_framework import serializers
from admins.models import Blog
from accounts.models import CustomUser



class BlogSerializer(serializers.ModelSerializer):
  
    class Meta:
      model = Blog
      fields = '__all__'
      
      

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
          'id',
          'email',
          'name',
          'phone',
          'gender',
          'is_active',
          'created_at'
        ]