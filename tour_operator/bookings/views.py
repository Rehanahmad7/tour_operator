from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Booking, Customer, CustomTourRequest
from tours.models import TourDate
from .forms import BookingForm, CustomTourRequestForm

@login_required
def book_tour(request, tour_date_id):
    tour_date = get_object_or_404(TourDate, id=tour_date_id, is_available=True)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            customer, created = Customer.objects.get_or_create(user=request.user)
            booking.customer = customer
            booking.tour_date = tour_date
            booking.total_price = tour_date.tour_package.price * booking.participants
            booking.save()

            tour_date.available_spots -= booking.participants
            tour_date.save()

            messages.success(request, 'Booking created successfully!')
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'bookings/book_tour.html', {
        'form': form,
        'tour_date': tour_date
    })

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer__user=request.user)
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})

@login_required
def my_bookings(request):
    try:
        customer = Customer.objects.get(user=request.user)
        bookings = Booking.objects.filter(customer=customer).order_by('-booking_date')
    except Customer.DoesNotExist:
        bookings = []
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def custom_tour_request(request):
    if request.method == 'POST':
        form = CustomTourRequestForm(request.POST)
        if form.is_valid():
            custom_request = form.save(commit=False)
            customer, created = Customer.objects.get_or_create(user=request.user)
            custom_request.customer = customer
            custom_request.save()
            messages.success(request, 'Custom tour request submitted successfully!')
            return redirect('home')
    else:
        form = CustomTourRequestForm()

    return render(request, 'bookings/custom_tour_request.html', {'form': form})
