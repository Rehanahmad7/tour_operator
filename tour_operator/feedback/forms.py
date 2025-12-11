from django import forms
from .models import TourFeedback, GuideFeedback

class TourFeedbackForm(forms.ModelForm):
    class Meta:
        model = TourFeedback
        fields = ['overall_rating', 'guide_rating', 'accommodation_rating', 'value_for_money_rating',
                 'comments', 'would_recommend', 'suggestions']
        widgets = {
            'overall_rating': forms.Select(attrs={'class': 'form-control'}),
            'guide_rating': forms.Select(attrs={'class': 'form-control'}),
            'accommodation_rating': forms.Select(attrs={'class': 'form-control'}),
            'value_for_money_rating': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'would_recommend': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'suggestions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class GuideFeedbackForm(forms.ModelForm):
    class Meta:
        model = GuideFeedback
        fields = ['knowledge_rating', 'communication_rating', 'professionalism_rating', 'comments']
        widgets = {
            'knowledge_rating': forms.Select(attrs={'class': 'form-control'}),
            'communication_rating': forms.Select(attrs={'class': 'form-control'}),
            'professionalism_rating': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }