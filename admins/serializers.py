from rest_framework import serializers
from admins.models import Blog,Activities
from accounts.models import CustomUser
from package.models import Booking,Package



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




# Admin Bookings List
class AdminBookingPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields =[
            'id','title','days','nights'
        ]

class AdminBookingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =[
            'id','name']    

class AdminBookingListSerializer(serializers.ModelSerializer):
    
    packge_data = AdminBookingPackageSerializer(source='booking_package', read_only=True)
    user_data = AdminBookingUserSerializer(source='user', read_only=True)


    class Meta:
        model = Booking
        fields = [
            'user_data', 'packge_data', 'booking_date', 'travel_start_date', 
            'travel_end_date', 'number_of_travelers', 'total_price', 
            'advance_amount', 'status', 'contact_number', 'email'
        ]




class ActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activities
        fields = ['activity','image','description','price']

    def update(self, instance, validated_data):
        instance.activity = validated_data.get('activity',instance.activity)
        instance.image = validated_data.get('image',instance.image)
        instance.description = validated_data.get('description',instance.description)
        instance.price = validated_data.get('price',instance.price)
        instance.save()
        return instance
    

class ActivityRetriveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activities
        fields = ['activity','image','description','price','rating']
