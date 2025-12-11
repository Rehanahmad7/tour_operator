from django.urls import path
from . import views

urlpatterns = [
    # Public guide views
    path('', views.guide_list, name='guide_list'),
    path('<int:guide_id>/', views.guide_profile, name='guide_profile'),
    path('<int:guide_id>/availability/', views.guide_availability_check, name='guide_availability_check'),

    # Guide dashboard views
    path('login/', views.guide_login, name='guide_login'),
    path('dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('bookings/', views.guide_bookings, name='guide_bookings'),
    path('schedule/', views.guide_schedule, name='guide_schedule'),
    path('feedback/', views.guide_feedback, name='guide_feedback'),
    path('profile/edit/', views.guide_profile_edit, name='guide_profile_edit'),
    path('logout/', views.guide_logout, name='guide_logout'),
]