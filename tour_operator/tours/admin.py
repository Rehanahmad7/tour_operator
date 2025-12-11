from django.contrib import admin
from .models import TourPackage, TourDate

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'duration', 'price', 'difficulty', 'max_participants', 'is_active']
    list_filter = ['difficulty', 'is_active', 'location']
    search_fields = ['name', 'location', 'description']
    list_editable = ['is_active', 'price']

@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ['tour_package', 'start_date', 'end_date', 'available_spots', 'is_available']
    list_filter = ['is_available', 'start_date']
    search_fields = ['tour_package__name']
    list_editable = ['available_spots', 'is_available']
