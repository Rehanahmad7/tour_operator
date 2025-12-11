from django.contrib import admin
from .models import Customer, Booking, CustomTourRequest

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'nationality', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'nationality']
    list_filter = ['nationality', 'created_at']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'tour_date', 'guide', 'participants', 'total_price', 'status', 'payment_status']
    list_filter = ['status', 'payment_status', 'booking_date']
    search_fields = ['customer__user__first_name', 'customer__user__last_name', 'tour_date__tour_package__name']
    list_editable = ['status', 'payment_status', 'guide']

@admin.register(CustomTourRequest)
class CustomTourRequestAdmin(admin.ModelAdmin):
    list_display = ['customer', 'destination', 'duration', 'participants', 'budget_range', 'is_processed']
    list_filter = ['is_processed', 'created_at']
    search_fields = ['customer__user__first_name', 'customer__user__last_name', 'destination']
    list_editable = ['is_processed']
