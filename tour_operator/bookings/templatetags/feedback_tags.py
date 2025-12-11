from django import template
from feedback.models import TourFeedback

register = template.Library()

@register.filter
def has_feedback(booking):
    """Check if the booking already has feedback submitted"""
    try:
        return TourFeedback.objects.filter(booking=booking).exists()
    except:
        return False