from rest_framework import serializers
from package.models import Package,DayDetail,Booking,Payment
from rest_framework.exceptions import ValidationError
from datetime import timedelta


class DayDetailSerializer(serializers.ModelSerializer):
    class Meta:
      model = DayDetail
      fields = ('package','day_number', 'description')
      

class PackageListSerializer(serializers.ModelSerializer):
    day_details = DayDetailSerializer(many=True, read_only=True)
    
    class Meta:
      model = Package
      fields = ('id','title', 'description', 'days', 'nights', 'price','day_details')
      
      
      
class PackageDetailSerializer(serializers.ModelSerializer):
    day_details = DayDetailSerializer(many=True, read_only=False)

    class Meta:
        model = Package
        fields = ('id', 'title', 'description', 'days', 'nights', 'price', 'day_details')

    def create(self, validated_data):
        # Extract day_details from validated_data
        day_details_data = validated_data.pop('day_details', [])
        
        # Create the Package instance
        package = Package.objects.create(**validated_data)
        
        # Create associated DayDetail instances
        for day_detail_data in day_details_data:
            DayDetail.objects.create(package=package, **day_detail_data)
        
        return package


# Bokking Retrive
class BookingRetriveSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Package
        fields = ['id','title','price','days','nights','min_members','max_members']

# Booking Creation
class BookingSerializer(serializers.ModelSerializer):
    package_data = BookingRetriveSerializer(source='booking_package', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id','travel_start_date',
                  'number_of_travelers','first_name','last_name','zip_code','contact_number','pro_noun',
                  'email','package_data']
        

    def validate(self, data):
        
        if 'travel_start_date' in data and 'travel_end_date' in data:
            if data['travel_start_date'] > data['travel_end_date']:
                raise serializers.ValidationError("Travel start date must be before the end date.")
        return data
    

# Booking List
class BookingListSerializer(serializers.ModelSerializer):
    package_data = BookingRetriveSerializer(source='booking_package', read_only=True)

    class Meta:
        model = Booking
        fields = ['id','package_data','travel_start_date','travel_end_date','number_of_travelers',
                  'booking_date','total_amount','payable_amount','advance_amount','balance_amount',
                  'contact_number','email','status']
        


# Booking updation
class BookingDetailsSerializer(serializers.ModelSerializer):
    """
    This nested serializer provides read-only access to specific details about a booking.
    """
    class Meta:
        model = Booking
        fields = ['booking_date', 'total_amount','payable_amount','advance_amount','balance_amount','status']
        read_only_fields = fields


class BookingUpdateSerializer(serializers.ModelSerializer):
    package_data = BookingRetriveSerializer(source='booking_package', read_only=True)
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

        new_travelers = validated_data.get('number_of_travelers',0)
        if new_travelers:
            updated_travelers = new_travelers + instance.number_of_travelers

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
            instance.payable_amount = updated_payable_amount

            # Ensure advance_amount is valid
            updated_advance = round(updated_payable_amount * 0.4)
            
            # Calculate balance_amount

            updated_balance = updated_payable_amount - updated_advance

            instance.advance_amount = updated_advance
            instance.balance_amount = updated_balance

            instance.number_of_travelers = updated_travelers
        instance.save()
        return instance

    



class PaymentSerializer(serializers.ModelSerializer):

    class Meta :
        model = Payment
        fields = []