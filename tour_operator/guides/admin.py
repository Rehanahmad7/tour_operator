from django.contrib import admin
from .models import Guide, GuideAvailability

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'experience_years', 'rating', 'is_available']
    list_filter = ['is_available', 'experience_years']
    search_fields = ['user__first_name', 'user__last_name', 'specializations']
    list_editable = ['is_available', 'rating']

@admin.register(GuideAvailability)
class GuideAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['guide', 'date', 'is_available']
    list_filter = ['is_available', 'date']
    search_fields = ['guide__user__first_name', 'guide__user__last_name']
