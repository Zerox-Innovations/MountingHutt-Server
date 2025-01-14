from rest_framework import serializers
from package.models import Package,DayDetail,Booking
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from rest_framework.response import Response

class DayDetailSerializer(serializers.ModelSerializer):
    class Meta:
      model = DayDetail
      fields = ['package','day_number', 'description']
      

class PackageListSerializer(serializers.ModelSerializer):
    day_details = DayDetailSerializer(many=True, read_only=True)
    
    class Meta:
      model = Package

      fields = ['id','title', 'description', 'days', 'nights', 'price','day_details']

      
      
      
class PackageDetailSerializer(serializers.ModelSerializer):
    day_details = DayDetailSerializer(many=True, read_only=False)

    class Meta:
        model = Package
        fields = ['id', 'title', 'description', 'days', 'nights', 'price', 'day_details']

    def create(self, validated_data):
        # Extract day_details from validated_data
        day_details_data = validated_data.pop('day_details', [])
        
        # Create the Package instance
        package = Package.objects.create(**validated_data)
        
        # Create associated DayDetail instances
        for day_detail_data in day_details_data:
            DayDetail.objects.create(package=package, **day_detail_data)
        
        return package



# p


# Packge image List
class PackageTitleSerializer(serializers.ModelSerializer):

    
    class Meta:
      model = Package
      fields = ['title']





# Bokking Retrive
class PackageRetriveForBookingSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Package
        fields = ['id','title','price','days','nights','min_members','max_members']






# Booking Creation
class BookingSerializer(serializers.ModelSerializer):
    package_data = PackageRetriveForBookingSerializer(source='booking_package', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id','travel_start_date',
                  'number_of_travelers','package_data']
        

    def validate(self, data):
        
        if 'travel_start_date' in data and 'travel_end_date' in data:
            if data['travel_start_date'] > data['travel_end_date']:
                raise serializers.ValidationError("Travel start date must be before the end date.")
        return data






# Booking Checkout

class UserDetailsCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['pro_noun', 'first_name', 'last_name', 'zip_code',
                  'contact_number', 'email']


class BookingCheckoutSerializer(serializers.ModelSerializer):
    user_details = UserDetailsCheckoutSerializer(write_only=True)  # Nested serializer for creating user details
    user_details_response = UserDetailsCheckoutSerializer(source='*', read_only=True)  # Used for the response
    package_data = PackageRetriveForBookingSerializer(source='booking_package', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'travel_start_date', 'travel_end_date', 'number_of_travelers',
            'created_at', 'total_amount', 'payable_amount', 'advance_amount',
            'balance_amount', 'status', 'user_details','user_details_response','package_data'
        ]

    def update(self, instance, validated_data):
        # Extract and pop user details if present
        user_details_data = validated_data.pop('user_details', None)

        # Update the Booking instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle user details if provided
        if user_details_data:
            user_details_instance = UserDetailsCheckoutSerializer(instance=instance, data=user_details_data)
            if user_details_instance.is_valid():
                user_details_instance.save()

        return instance


        







# Booking List
class BookingListSerializer(serializers.ModelSerializer):
    package_data = PackageRetriveForBookingSerializer(source='booking_package', read_only=True)
    

    class Meta:
        model = Booking
        fields = ['id','package_data','travel_start_date','travel_end_date','number_of_travelers',
                  'created_at','total_amount','payable_amount','advance_amount','balance_amount',
                  'contact_number','email','status']
        








# Booking updation
class NonRefundableAdvanceError(Exception):
    pass


class BookingDetailsSerializer(serializers.ModelSerializer):
    """
    This nested serializer provides read-only access to specific details about a booking.
    """
    class Meta:
        model = Booking
        fields = ['created_at', 'total_amount','payable_amount','advance_amount','balance_amount','status']
        read_only_fields = fields


class BookingUpdateSerializer(serializers.ModelSerializer):
    package_data = PackageRetriveForBookingSerializer(source='booking_package', read_only=True)
    booking_data = BookingDetailsSerializer(source='*', read_only=True) 

    class Meta:
        model = Booking
        fields = ['travel_start_date','travel_end_date','number_of_travelers','contact_number','email',
                  'booking_data','package_data']


    def update(self, instance, validated_data):
        instance.travel_start_date = validated_data.get('travel_start_date', instance.travel_start_date)

        booking_package = instance.booking_package
        total_days = booking_package.nights
        instance.travel_end_date = instance.travel_start_date + timedelta(days=total_days)

        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.email = validated_data.get('email', instance.email)

        updated_travelers = validated_data.get('number_of_travelers',instance.number_of_travelers)
        if updated_travelers:
            
            min_members = booking_package.min_members
            if updated_travelers < min_members:
                raise ValidationError({"Msg": f"Should have a minimum of {min_members} members"})
            max_members = booking_package.max_members
            if max_members is not None and updated_travelers > max_members:
                raise ValidationError({"Msg": f"The maximum number of members allowed is {max_members}"})
            
            base_price = booking_package.price
            updated_total_amount = base_price * updated_travelers
            instance.total_amount = updated_total_amount

            decrement = (updated_travelers) * 200 if updated_travelers > 4 else 0
            updated_payable_amount = updated_total_amount - decrement
            

            # Ensure advance_amount is valid
            updated_advance = round(updated_payable_amount * 0.4)
            if updated_advance < instance.advance_amount:
                canceled_Members = instance.number_of_travelers - updated_travelers
                not_refund = round((instance.payable_amount * 0.4) / instance.number_of_travelers * canceled_Members)
                
                
                

            updated_balance = updated_payable_amount - updated_advance

            instance.payable_amount = updated_payable_amount
            instance.advance_amount = updated_advance
            instance.balance_amount = updated_balance

            instance.number_of_travelers = updated_travelers
        instance.save()
        return instance

    


