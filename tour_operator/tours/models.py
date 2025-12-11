from django.db import models
from django.contrib.auth.models import User

class TourPackage(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('difficult', 'Difficult'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_participants = models.IntegerField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    location = models.CharField(max_length=200)
    included_services = models.TextField()
    excluded_services = models.TextField()
    itinerary = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_primary_image(self):
        """Get the primary image for this tour"""
        primary_image = self.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image_url
        # If no primary image, return the first image
        first_image = self.images.first()
        return first_image.image_url if first_image else None

    def get_all_images(self):
        """Get all images for this tour ordered by display_order"""
        return self.images.all()

class TourDate(models.Model):
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='tour_dates')
    start_date = models.DateField()
    end_date = models.DateField()
    available_spots = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tour_package.name} - {self.start_date} to {self.end_date}"

class TourImage(models.Model):
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500, help_text="URL of the tour image")
    caption = models.CharField(max_length=200, blank=True, help_text="Optional image caption")
    is_primary = models.BooleanField(default=False, help_text="Set as primary/featured image")
    display_order = models.PositiveIntegerField(default=0, help_text="Order in which images are displayed")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'created_at']

    def __str__(self):
        return f"{self.tour_package.name} - Image {self.display_order}"

    def save(self, *args, **kwargs):
        # If this is set as primary, remove primary flag from other images of the same tour
        if self.is_primary:
            TourImage.objects.filter(tour_package=self.tour_package, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
