from django.contrib import admin
from package.models import DayDetail, Package

@admin.register(Package)
class PackagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'days', 'nights', 'price', 'created_at', 'updated_at')

@admin.register(DayDetail)
class DayDetailAdmin(admin.ModelAdmin):
    list_display = ('day_number', 'description', 'package')
