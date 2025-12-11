from django import forms
from .models import Booking, CustomTourRequest, Customer

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['participants', 'special_requests']
        widgets = {
            'participants': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Any special requirements or requests...'}),
        }

class CustomTourRequestForm(forms.ModelForm):
    class Meta:
        model = CustomTourRequest
        fields = ['destination', 'duration', 'participants', 'budget_range', 'preferred_dates', 'special_requirements']
        widgets = {
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'participants': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'budget_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., ₹1000-2000'}),
            'preferred_dates': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., March 2024'}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone', 'emergency_contact', 'emergency_phone', 'date_of_birth', 'nationality', 'passport_number']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
        }