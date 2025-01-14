from admins.models import Activities,Food,Room
from rest_framework import serializers




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


