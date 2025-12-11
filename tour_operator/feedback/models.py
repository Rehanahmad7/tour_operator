from django.db import models
from bookings.models import Booking
from guides.models import Guide

class TourFeedback(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    overall_rating = models.IntegerField(choices=RATING_CHOICES)
    guide_rating = models.IntegerField(choices=RATING_CHOICES)
    accommodation_rating = models.IntegerField(choices=RATING_CHOICES)
    value_for_money_rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField()
    would_recommend = models.BooleanField()
    suggestions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.booking} - Rating: {self.overall_rating}/5"

class GuideFeedback(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='feedback_received')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    knowledge_rating = models.IntegerField(choices=RATING_CHOICES)
    communication_rating = models.IntegerField(choices=RATING_CHOICES)
    professionalism_rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Guide Feedback for {self.guide} from {self.booking}"
