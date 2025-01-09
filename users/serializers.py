from admins.models import Activities,Food,Room
from rest_framework import serializers
from package.models import Booking,Package



class UserActivitySerializer(serializers.ModelSerializer):

    class Meta :
        model = Activities
        fields =['activity','image','description','price']



class UserFoodSerializer(serializers.ModelSerializer):

    class Meta :
        model = Food
        fields =['item','image','description','time','category','price']



class UserRoomSerializer(serializers.ModelSerializer):

    class Meta :
        model = Room
        fields =['room_name','image','capacity','description','price']


class PackageBookingHistorySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Package
        fields = ['id','title','price','days','nights','min_members','max_members']


class BookingHistorySerializer(serializers.ModelSerializer):
    package_data = PackageBookingHistorySerializer(source='booking_package', read_only=True)
    

    class Meta:
        model = Booking
        fields = ['id','package_data','travel_start_date','travel_end_date','number_of_travelers',
                  'created_at','total_amount','payable_amount','advance_amount','balance_amount',
                  'contact_number','email','status']