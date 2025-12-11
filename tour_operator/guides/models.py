from django.db import models
from django.contrib.auth.models import User

class Guide(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    experience_years = models.IntegerField()
    languages = models.CharField(max_length=200, help_text="Comma-separated languages")
    specializations = models.CharField(max_length=300, help_text="Areas of expertise")
    bio = models.TextField()
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class GuideAvailability(models.Model):
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('guide', 'date')

    def __str__(self):
        return f"{self.guide} - {self.date} ({'Available' if self.is_available else 'Unavailable'})"
