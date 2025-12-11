from django.contrib import admin
from .models import TourFeedback, GuideFeedback

@admin.register(TourFeedback)
class TourFeedbackAdmin(admin.ModelAdmin):
    list_display = ['booking', 'overall_rating', 'guide_rating', 'would_recommend', 'created_at']
    list_filter = ['overall_rating', 'guide_rating', 'would_recommend', 'created_at']
    search_fields = ['booking__customer__user__first_name', 'booking__customer__user__last_name', 'booking__tour_date__tour_package__name']
    readonly_fields = ['booking', 'created_at']

@admin.register(GuideFeedback)
class GuideFeedbackAdmin(admin.ModelAdmin):
    list_display = ['guide', 'booking', 'knowledge_rating', 'communication_rating', 'professionalism_rating', 'created_at']
    list_filter = ['knowledge_rating', 'communication_rating', 'professionalism_rating', 'created_at']
    search_fields = ['guide__user__first_name', 'guide__user__last_name', 'booking__customer__user__first_name']
    readonly_fields = ['guide', 'booking', 'created_at']
