from django.db import models
from django.contrib.auth.models import User
from tours.models import TourDate
from guides.models import Guide

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tour_date = models.ForeignKey(TourDate, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking {self.id} - {self.customer} - {self.tour_date.tour_package.name}"

class CustomTourRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    destination = models.CharField(max_length=200)
    duration = models.IntegerField(help_text="Duration in days")
    participants = models.IntegerField()
    budget_range = models.CharField(max_length=100)
    preferred_dates = models.CharField(max_length=200)
    special_requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Custom Tour Request - {self.customer} - {self.destination}"
