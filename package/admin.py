from django.contrib import admin
from package.models import DayDetail, Package , Booking , Payment

@admin.register(Package)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description', 'days', 'nights', 'price', 'created_at', 'updated_at')

@admin.register(DayDetail)
class DayDetailAdmin(admin.ModelAdmin):
    list_display = ('day_number', 'description', 'package')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'booking_package', 'status')


@admin.register(Payment)
class PaymentgAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'booking_data', 'payment_status')
