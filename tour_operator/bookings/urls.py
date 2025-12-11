from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:tour_date_id>/', views.book_tour, name='book_tour'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('custom-tour/', views.custom_tour_request, name='custom_tour_request'),
]