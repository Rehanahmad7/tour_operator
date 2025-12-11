from django.urls import path
from . import views

urlpatterns = [
    path('submit/<int:booking_id>/', views.submit_feedback, name='submit_feedback'),
    path('reviews/', views.feedback_list, name='feedback_list'),
]