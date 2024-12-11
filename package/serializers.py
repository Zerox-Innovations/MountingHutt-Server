from rest_framework import serializers
from package.models import Package,DayDetail




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
        day_details_data = validated_data.pop('day_details', [])
        package = Package.objects.create(**validated_data)
        
        for day_detail_data in day_details_data:
            DayDetail.objects.create(package=package, **day_detail_data)

        return package
