from rest_framework import serializers
from admins.models import Blog,Activities,Food,Item_category,Room
from accounts.models import CustomUser
from package.models import Booking,Package



class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'image']  

class BlogDetailSerializer(serializers.ModelSerializer):
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
            'user_data', 'packge_data', 'created_at', 'travel_start_date', 
            'travel_end_date', 'number_of_travelers', 'total_amount', 
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
        fields = ['activity','image','description','price']




class AdminFoodSerializer(serializers.ModelSerializer):
    time = serializers.CharField() 

    class Meta:
        model = Food
        fields =['item','image','description','time','category','price']

    def update(self, instance, validated_data):
        instance.item = validated_data.get('item',instance.item)
        instance.image = validated_data.get('image',instance.image)
        instance.description = validated_data.get('description',instance.description)
        instance.time = validated_data.get('time',instance.time)
        instance.category = validated_data.get('category',instance.category)
        instance.price = validated_data.get('price',instance.price)
        instance.save()
        return instance


    def validate_time(self, value):
        """
        Validate the `time` field to ensure the string maps to a valid `Item_category` instance.
        """
        try:
            time_instance = Item_category.objects.get(food_time__iexact=value)
            return time_instance # Return the instance to be set in the `time` field
        except Item_category.DoesNotExist:
            raise serializers.ValidationError(f"Invalid time reference. No such time: {value}.")

    def validate_category(self, value):
        # Ensure the category is one of the valid choices
        valid_choices = dict(Food._meta.get_field('category').choices)
        if value not in valid_choices:
            raise serializers.ValidationError(f"Invalid category. Choose from {list(valid_choices.keys())}.")
        return value
    



class AdminFoodRetriveSerializer(serializers.ModelSerializer):
 

    class Meta:
        model = Food
        fields =['item','image','description','time','category','price']




class AdminRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['room_name','capacity','image','description','price']

    def update(self, instance, validated_data):
        instance.room_name = validated_data.get('room_name',instance.room_name)
        instance.image = validated_data.get('image',instance.image)
        instance.capacity = validated_data.get('capacity',instance.capacity)
        instance.description = validated_data.get('description',instance.description)
        instance.price = validated_data.get('price',instance.price)
        instance.save()
        return instance
    





class AdminRoomRetriveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['room_name','image','capacity','description','price']