from rest_framework import serializers
from .models import Package, DayDetail


class DayDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayDetail
        fields = ('id', 'day_number', 'description')  # Exclude 'package' from the input
        read_only_fields = ('id',)  # Mark 'id' as read-only



class PackageListSerializer(serializers.ModelSerializer):
    day_details = DayDetailSerializer(many=True)  # Make day_details writable

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

    def update(self, instance, validated_data):
        # Extract day_details from validated_data
        day_details_data = validated_data.pop('day_details', [])
        
        # Update Package instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or recreate DayDetail instances
        existing_ids = set(instance.day_details.values_list('id', flat=True))
        new_ids = {item.get('id') for item in day_details_data if item.get('id')}

        # Delete DayDetail instances not in new data
        DayDetail.objects.filter(id__in=existing_ids - new_ids).delete()

        # Create or update DayDetail instances
        for day_detail_data in day_details_data:
            if day_detail_data.get('id') in existing_ids:
                # Update existing record
                day_detail_instance = DayDetail.objects.get(id=day_detail_data['id'])
                for attr, value in day_detail_data.items():
                    setattr(day_detail_instance, attr, value)
                day_detail_instance.save()
            else:
                # Create new record
                DayDetail.objects.create(package=instance, **day_detail_data)
        
        return instance

