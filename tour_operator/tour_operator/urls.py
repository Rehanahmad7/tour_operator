"""
URL configuration for tour_operator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tours.views import home
from .auth_views import signup
from .admin_views import (
    admin_login, admin_dashboard, admin_tour_list, admin_create_tour,
    admin_edit_tour, admin_tour_dates, admin_bookings, admin_booking_detail,
    admin_custom_requests, admin_process_custom_request, admin_logout,
    admin_guides, admin_create_guide, admin_edit_guide, admin_guide_detail,
    admin_guide_availability, admin_assign_guide, admin_feedback,
    admin_feedback_detail, admin_guide_feedback
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('tours/', include('tours.urls')),
    path('bookings/', include('bookings.urls')),
    path('guides/', include('guides.urls')),
    path('feedback/', include('feedback.urls')),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Custom admin URLs
    path('tour-admin/', admin_login, name='admin_login'),
    path('tour-admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('tour-admin/logout/', admin_logout, name='admin_logout'),
    path('tour-admin/tours/', admin_tour_list, name='admin_tour_list'),
    path('tour-admin/tours/create/', admin_create_tour, name='admin_create_tour'),
    path('tour-admin/tours/<int:tour_id>/edit/', admin_edit_tour, name='admin_edit_tour'),
    path('tour-admin/tours/<int:tour_id>/dates/', admin_tour_dates, name='admin_tour_dates'),
    path('tour-admin/bookings/', admin_bookings, name='admin_bookings'),
    path('tour-admin/bookings/<int:booking_id>/', admin_booking_detail, name='admin_booking_detail'),
    path('tour-admin/custom-requests/', admin_custom_requests, name='admin_custom_requests'),
    path('tour-admin/custom-requests/<int:request_id>/process/', admin_process_custom_request, name='admin_process_custom_request'),

    # Guide management URLs
    path('tour-admin/guides/', admin_guides, name='admin_guides'),
    path('tour-admin/guides/create/', admin_create_guide, name='admin_create_guide'),
    path('tour-admin/guides/<int:guide_id>/edit/', admin_edit_guide, name='admin_edit_guide'),
    path('tour-admin/guides/<int:guide_id>/', admin_guide_detail, name='admin_guide_detail'),
    path('tour-admin/guides/<int:guide_id>/availability/', admin_guide_availability, name='admin_guide_availability'),
    path('tour-admin/bookings/<int:booking_id>/assign-guide/', admin_assign_guide, name='admin_assign_guide'),

    # Feedback management URLs
    path('tour-admin/feedback/', admin_feedback, name='admin_feedback'),
    path('tour-admin/feedback/<int:feedback_id>/', admin_feedback_detail, name='admin_feedback_detail'),
    path('tour-admin/guide-feedback/', admin_guide_feedback, name='admin_guide_feedback'),
]
