from django.contrib import admin
from accounts.models import CustomUser


@admin.register(CustomUser)
class BusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")