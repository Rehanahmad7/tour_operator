from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import TourPackage, TourDate

def tour_list(request):
    tours = TourPackage.objects.filter(is_active=True)
    return render(request, 'tours/tour_list.html', {'tours': tours})

def tour_detail(request, tour_id):
    tour = get_object_or_404(TourPackage, id=tour_id, is_active=True)
    tour_dates = TourDate.objects.filter(tour_package=tour, is_available=True)
    return render(request, 'tours/tour_detail.html', {
        'tour': tour,
        'tour_dates': tour_dates
    })

def home(request):
    featured_tours = TourPackage.objects.filter(is_active=True)[:6]
    return render(request, 'tours/home.html', {'featured_tours': featured_tours})
