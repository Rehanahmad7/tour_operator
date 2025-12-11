from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from tours.models import TourPackage, TourDate, TourImage
from bookings.models import Booking, Customer, CustomTourRequest
from guides.models import Guide, GuideAvailability
from feedback.models import TourFeedback, GuideFeedback
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta
from django.db.models import Avg, Count, Q

# Hardcoded admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # Create or get admin user
            admin_user, created = User.objects.get_or_create(
                username=ADMIN_USERNAME,
                defaults={
                    'is_staff': True,
                    'is_superuser': True,
                    'first_name': 'Admin',
                    'last_name': 'User'
                }
            )
            if created:
                admin_user.set_password(ADMIN_PASSWORD)
                admin_user.save()

            login(request, admin_user)
            messages.success(request, 'Welcome, Admin!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials.')

    return render(request, 'admin/admin_login.html')

def is_admin(user):
    return user.is_authenticated and user.username == ADMIN_USERNAME

@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_login')

    # Dashboard statistics
    total_tours = TourPackage.objects.count()
    active_tours = TourPackage.objects.filter(is_active=True).count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    total_customers = Customer.objects.count()
    custom_requests = CustomTourRequest.objects.filter(is_processed=False).count()
    total_guides = Guide.objects.count()
    available_guides = Guide.objects.filter(is_available=True).count()
    total_feedback = TourFeedback.objects.count()
    avg_rating = TourFeedback.objects.aggregate(avg_rating=Avg('overall_rating'))['avg_rating'] or 0

    context = {
        'total_tours': total_tours,
        'active_tours': active_tours,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'total_customers': total_customers,
        'custom_requests': custom_requests,
        'total_guides': total_guides,
        'available_guides': available_guides,
        'total_feedback': total_feedback,
        'avg_rating': round(avg_rating, 1),
    }

    return render(request, 'admin/admin_dashboard.html', context)

@login_required
def admin_tour_list(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    tours = TourPackage.objects.all().order_by('-created_at')
    return render(request, 'admin/tour_list.html', {'tours': tours})

@login_required
def admin_create_tour(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    if request.method == 'POST':
        # Create tour package
        tour = TourPackage.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            duration=int(request.POST.get('duration')),
            price=float(request.POST.get('price')),
            max_participants=int(request.POST.get('max_participants')),
            difficulty=request.POST.get('difficulty'),
            location=request.POST.get('location'),
            included_services=request.POST.get('included_services'),
            excluded_services=request.POST.get('excluded_services'),
            itinerary=request.POST.get('itinerary'),
            is_active=request.POST.get('is_active') == 'on'
        )

        # Handle multiple images
        image_urls = request.POST.getlist('image_urls')
        image_captions = request.POST.getlist('image_captions')
        primary_image_index = request.POST.get('primary_image')

        for i, url in enumerate(image_urls):
            if url.strip():  # Only create if URL is not empty
                caption = image_captions[i] if i < len(image_captions) else ''
                is_primary = str(i) == primary_image_index
                TourImage.objects.create(
                    tour_package=tour,
                    image_url=url.strip(),
                    caption=caption.strip(),
                    is_primary=is_primary,
                    display_order=i
                )

        messages.success(request, f'Tour "{tour.name}" created successfully with {len([url for url in image_urls if url.strip()])} images!')
        return redirect('admin_tour_list')

    return render(request, 'admin/create_tour.html')

@login_required
def admin_edit_tour(request, tour_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    tour = get_object_or_404(TourPackage, id=tour_id)

    if request.method == 'POST':
        tour.name = request.POST.get('name')
        tour.description = request.POST.get('description')
        tour.duration = int(request.POST.get('duration'))
        tour.price = float(request.POST.get('price'))
        tour.max_participants = int(request.POST.get('max_participants'))
        tour.difficulty = request.POST.get('difficulty')
        tour.location = request.POST.get('location')
        tour.included_services = request.POST.get('included_services')
        tour.excluded_services = request.POST.get('excluded_services')
        tour.itinerary = request.POST.get('itinerary')
        tour.is_active = request.POST.get('is_active') == 'on'
        tour.save()

        # Handle image updates - first remove all existing images
        tour.images.all().delete()

        # Then add new images
        image_urls = request.POST.getlist('image_urls')
        image_captions = request.POST.getlist('image_captions')
        primary_image_index = request.POST.get('primary_image')

        for i, url in enumerate(image_urls):
            if url.strip():  # Only create if URL is not empty
                caption = image_captions[i] if i < len(image_captions) else ''
                is_primary = str(i) == primary_image_index
                TourImage.objects.create(
                    tour_package=tour,
                    image_url=url.strip(),
                    caption=caption.strip(),
                    is_primary=is_primary,
                    display_order=i
                )

        messages.success(request, f'Tour "{tour.name}" updated successfully with {len([url for url in image_urls if url.strip()])} images!')
        return redirect('admin_tour_list')

    return render(request, 'admin/edit_tour.html', {'tour': tour})

@login_required
def admin_tour_dates(request, tour_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    tour = get_object_or_404(TourPackage, id=tour_id)
    tour_dates = TourDate.objects.filter(tour_package=tour).order_by('start_date')

    if request.method == 'POST':
        # Add new tour date
        TourDate.objects.create(
            tour_package=tour,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            available_spots=int(request.POST.get('available_spots')),
            is_available=request.POST.get('is_available') == 'on'
        )
        messages.success(request, 'Tour date added successfully!')
        return redirect('admin_tour_dates', tour_id=tour.id)

    return render(request, 'admin/tour_dates.html', {
        'tour': tour,
        'tour_dates': tour_dates
    })

@login_required
def admin_bookings(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    bookings = Booking.objects.all().order_by('-booking_date').select_related('customer', 'tour_date', 'guide')
    return render(request, 'admin/bookings.html', {'bookings': bookings})

@login_required
def admin_booking_detail(request, booking_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        # Update booking status
        booking.status = request.POST.get('status')
        booking.payment_status = request.POST.get('payment_status') == 'on'
        booking.save()

        messages.success(request, 'Booking updated successfully!')
        return redirect('admin_bookings')

    return render(request, 'admin/booking_detail.html', {'booking': booking})

@login_required
def admin_custom_requests(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    custom_requests = CustomTourRequest.objects.all().order_by('-created_at').select_related('customer')
    return render(request, 'admin/custom_requests.html', {'custom_requests': custom_requests})

@login_required
def admin_process_custom_request(request, request_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    custom_request = get_object_or_404(CustomTourRequest, id=request_id)
    custom_request.is_processed = True
    custom_request.save()

    messages.success(request, 'Custom tour request marked as processed!')
    return redirect('admin_custom_requests')

def admin_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('admin_login')

# Guide Management Views
@login_required
def admin_guides(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    guides = Guide.objects.all().order_by('-created_at').select_related('user')
    return render(request, 'admin/guides.html', {'guides': guides})

@login_required
def admin_create_guide(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    if request.method == 'POST':
        # Create user first
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'admin/create_guide.html')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Create guide profile
        Guide.objects.create(
            user=user,
            phone=request.POST.get('phone'),
            experience_years=int(request.POST.get('experience_years')),
            languages=request.POST.get('languages'),
            specializations=request.POST.get('specializations'),
            bio=request.POST.get('bio'),
            is_available=request.POST.get('is_available') == 'on',
            rating=float(request.POST.get('rating', 0))
        )

        messages.success(request, f'Guide "{first_name} {last_name}" created successfully!')
        return redirect('admin_guides')

    return render(request, 'admin/create_guide.html')

@login_required
def admin_edit_guide(request, guide_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    guide = get_object_or_404(Guide, id=guide_id)

    if request.method == 'POST':
        # Update user information
        guide.user.first_name = request.POST.get('first_name')
        guide.user.last_name = request.POST.get('last_name')
        guide.user.email = request.POST.get('email')
        guide.user.save()

        # Update guide profile
        guide.phone = request.POST.get('phone')
        guide.experience_years = int(request.POST.get('experience_years'))
        guide.languages = request.POST.get('languages')
        guide.specializations = request.POST.get('specializations')
        guide.bio = request.POST.get('bio')
        guide.is_available = request.POST.get('is_available') == 'on'
        guide.rating = float(request.POST.get('rating', 0))
        guide.save()

        messages.success(request, f'Guide "{guide.user.first_name} {guide.user.last_name}" updated successfully!')
        return redirect('admin_guides')

    return render(request, 'admin/edit_guide.html', {'guide': guide})

@login_required
def admin_guide_detail(request, guide_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    guide = get_object_or_404(Guide, id=guide_id)
    bookings = Booking.objects.filter(guide=guide).order_by('-booking_date')[:10]

    return render(request, 'admin/guide_detail.html', {
        'guide': guide,
        'bookings': bookings
    })

@login_required
def admin_guide_availability(request, guide_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    guide = get_object_or_404(Guide, id=guide_id)

    if request.method == 'POST':
        availability_date = request.POST.get('date')
        is_available = request.POST.get('is_available') == 'on'

        availability, created = GuideAvailability.objects.get_or_create(
            guide=guide,
            date=availability_date,
            defaults={'is_available': is_available}
        )

        if not created:
            availability.is_available = is_available
            availability.save()

        messages.success(request, f'Availability updated for {availability_date}')
        return redirect('admin_guide_availability', guide_id=guide.id)

    # Get availability for next 30 days
    availability_dates = []
    today = date.today()
    for i in range(30):
        check_date = today + timedelta(days=i)
        try:
            availability = GuideAvailability.objects.get(guide=guide, date=check_date)
            is_available = availability.is_available
        except GuideAvailability.DoesNotExist:
            is_available = True  # Default to available

        availability_dates.append({
            'date': check_date,
            'is_available': is_available
        })

    return render(request, 'admin/guide_availability.html', {
        'guide': guide,
        'availability_dates': availability_dates
    })

@login_required
def admin_assign_guide(request, booking_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    booking = get_object_or_404(Booking, id=booking_id)
    available_guides = Guide.objects.filter(is_available=True)

    if request.method == 'POST':
        guide_id = request.POST.get('guide_id')
        if guide_id:
            guide = get_object_or_404(Guide, id=guide_id)
            booking.guide = guide
            booking.save()
            messages.success(request, f'Guide {guide.user.first_name} {guide.user.last_name} assigned to booking #{booking.id}')
        else:
            booking.guide = None
            booking.save()
            messages.success(request, f'Guide removed from booking #{booking.id}')

        return redirect('admin_booking_detail', booking_id=booking.id)

    return render(request, 'admin/assign_guide.html', {
        'booking': booking,
        'available_guides': available_guides
    })

# Feedback Management Views
@login_required
def admin_feedback(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    tour_feedbacks = TourFeedback.objects.all().order_by('-created_at').select_related(
        'booking__customer__user',
        'booking__tour_date__tour_package'
    )

    # Get filter parameters
    rating_filter = request.GET.get('rating')
    tour_filter = request.GET.get('tour')

    if rating_filter:
        tour_feedbacks = tour_feedbacks.filter(overall_rating=rating_filter)

    if tour_filter:
        tour_feedbacks = tour_feedbacks.filter(booking__tour_date__tour_package__id=tour_filter)

    # Get available tours for filter
    available_tours = TourPackage.objects.all().order_by('name')

    # Calculate statistics
    stats = TourFeedback.objects.aggregate(
        avg_overall=Avg('overall_rating'),
        avg_guide=Avg('guide_rating'),
        avg_accommodation=Avg('accommodation_rating'),
        avg_value=Avg('value_for_money_rating'),
        total_count=Count('id'),
        recommend_count=Count('id', filter=Q(would_recommend=True))
    )

    recommend_percentage = 0
    if stats['total_count'] > 0:
        recommend_percentage = round((stats['recommend_count'] / stats['total_count']) * 100, 1)

    context = {
        'tour_feedbacks': tour_feedbacks,
        'available_tours': available_tours,
        'stats': stats,
        'recommend_percentage': recommend_percentage,
        'current_rating_filter': rating_filter,
        'current_tour_filter': tour_filter,
    }

    return render(request, 'admin/feedback.html', context)

@login_required
def admin_feedback_detail(request, feedback_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    feedback = get_object_or_404(TourFeedback, id=feedback_id)
    guide_feedback = None

    if feedback.booking.guide:
        try:
            guide_feedback = GuideFeedback.objects.get(booking=feedback.booking)
        except GuideFeedback.DoesNotExist:
            pass

    return render(request, 'admin/feedback_detail.html', {
        'feedback': feedback,
        'guide_feedback': guide_feedback
    })

@login_required
def admin_guide_feedback(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('admin_login')

    guide_feedbacks = GuideFeedback.objects.all().order_by('-created_at').select_related(
        'guide__user',
        'booking__customer__user',
        'booking__tour_date__tour_package'
    )

    # Calculate guide performance statistics
    guide_stats = {}
    for guide in Guide.objects.all():
        guide_feedback_qs = GuideFeedback.objects.filter(guide=guide)
        if guide_feedback_qs.exists():
            avg_knowledge = guide_feedback_qs.aggregate(avg=Avg('knowledge_rating'))['avg']
            avg_communication = guide_feedback_qs.aggregate(avg=Avg('communication_rating'))['avg']
            avg_professionalism = guide_feedback_qs.aggregate(avg=Avg('professionalism_rating'))['avg']

            guide_stats[guide.id] = {
                'avg_knowledge': round(avg_knowledge, 1) if avg_knowledge else 0,
                'avg_communication': round(avg_communication, 1) if avg_communication else 0,
                'avg_professionalism': round(avg_professionalism, 1) if avg_professionalism else 0,
                'total_feedback': guide_feedback_qs.count()
            }

    return render(request, 'admin/guide_feedback.html', {
        'guide_feedbacks': guide_feedbacks,
        'guide_stats': guide_stats
    })