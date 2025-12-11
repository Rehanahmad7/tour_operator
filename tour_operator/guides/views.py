from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .models import Guide, GuideAvailability
from bookings.models import Booking
from feedback.models import GuideFeedback
from tours.models import TourDate, TourPackage
from datetime import date, timedelta
from django.db.models import Avg, Count, Q

def guide_list(request):
    """Display all available guides"""
    guides = Guide.objects.filter(is_available=True).order_by('-rating')
    return render(request, 'guides/guide_list.html', {'guides': guides})

def guide_profile(request, guide_id):
    """Display detailed guide profile"""
    guide = get_object_or_404(Guide, id=guide_id, is_available=True)

    # Get recent feedback
    recent_feedback = GuideFeedback.objects.filter(guide=guide).order_by('-created_at')[:5]

    # Get recent tours/bookings
    recent_bookings = Booking.objects.filter(
        guide=guide,
        status__in=['completed', 'confirmed']
    ).order_by('-booking_date')[:5]

    # Calculate average ratings from feedback
    feedback_count = recent_feedback.count()
    avg_knowledge = 0
    avg_communication = 0
    avg_professionalism = 0

    if feedback_count > 0:
        knowledge_total = sum([f.knowledge_rating for f in recent_feedback])
        communication_total = sum([f.communication_rating for f in recent_feedback])
        professionalism_total = sum([f.professionalism_rating for f in recent_feedback])

        avg_knowledge = round(knowledge_total / feedback_count, 1)
        avg_communication = round(communication_total / feedback_count, 1)
        avg_professionalism = round(professionalism_total / feedback_count, 1)

    context = {
        'guide': guide,
        'recent_feedback': recent_feedback,
        'recent_bookings': recent_bookings,
        'feedback_count': feedback_count,
        'avg_knowledge': avg_knowledge,
        'avg_communication': avg_communication,
        'avg_professionalism': avg_professionalism,
    }

    return render(request, 'guides/guide_profile.html', context)

def guide_availability_check(request, guide_id):
    """Check guide availability for specific dates via AJAX"""
    if request.method == 'GET':
        guide = get_object_or_404(Guide, id=guide_id)
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            try:
                start_date = date.fromisoformat(start_date)
                end_date = date.fromisoformat(end_date)

                # Check if guide is available for all dates in range
                is_available = True
                unavailable_dates = []

                current_date = start_date
                while current_date <= end_date:
                    try:
                        availability = GuideAvailability.objects.get(
                            guide=guide,
                            date=current_date
                        )
                        if not availability.is_available:
                            is_available = False
                            unavailable_dates.append(current_date.isoformat())
                    except GuideAvailability.DoesNotExist:
                        # If no record exists, assume available
                        pass

                    current_date += timedelta(days=1)

                return JsonResponse({
                    'available': is_available,
                    'unavailable_dates': unavailable_dates,
                    'guide_name': f"{guide.user.first_name} {guide.user.last_name}"
                })

            except ValueError:
                return JsonResponse({'error': 'Invalid date format'}, status=400)

        return JsonResponse({'error': 'Missing date parameters'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Guide Dashboard Views
@csrf_protect
def guide_login(request):
    """Guide login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                guide = Guide.objects.get(user=user)
                login(request, user)
                messages.success(request, f'Welcome back, {guide.user.first_name}!')
                return redirect('guide_dashboard')
            except Guide.DoesNotExist:
                messages.error(request, 'You are not registered as a guide. Please contact admin.')
        else:
            messages.error(request, 'Invalid username or password.')

    # Pass any context if needed
    context = {
        'form_action': request.path,
    }
    return render(request, 'guides/guide_login.html', context)

def is_guide(user):
    """Check if user is a guide"""
    if not user.is_authenticated:
        return False
    try:
        Guide.objects.get(user=user)
        return True
    except Guide.DoesNotExist:
        return False

@login_required
def guide_dashboard(request):
    """Guide dashboard showing overview of tours, bookings, and feedback"""
    if not is_guide(request.user):
        messages.error(request, 'Access denied. Guide privileges required.')
        return redirect('guide_login')

    guide = Guide.objects.get(user=request.user)

    # Get statistics
    total_bookings = Booking.objects.filter(guide=guide).count()
    upcoming_bookings = Booking.objects.filter(
        guide=guide,
        tour_date__start_date__gte=date.today(),
        status__in=['confirmed', 'pending']
    ).count()
    completed_tours = Booking.objects.filter(
        guide=guide,
        status='completed'
    ).count()

    # Get feedback stats
    feedback_stats = GuideFeedback.objects.filter(guide=guide).aggregate(
        avg_knowledge=Avg('knowledge_rating'),
        avg_communication=Avg('communication_rating'),
        avg_professionalism=Avg('professionalism_rating'),
        total_feedback=Count('id')
    )

    # Get recent bookings
    recent_bookings = Booking.objects.filter(guide=guide).order_by('-booking_date')[:5]

    # Get upcoming tours
    upcoming_tours = Booking.objects.filter(
        guide=guide,
        tour_date__start_date__gte=date.today(),
        status__in=['confirmed', 'pending']
    ).order_by('tour_date__start_date')[:5]

    context = {
        'guide': guide,
        'total_bookings': total_bookings,
        'upcoming_bookings': upcoming_bookings,
        'completed_tours': completed_tours,
        'feedback_stats': feedback_stats,
        'recent_bookings': recent_bookings,
        'upcoming_tours': upcoming_tours,
    }

    return render(request, 'guides/guide_dashboard.html', context)

@login_required
def guide_bookings(request):
    """View all guide's bookings with filtering options"""
    if not is_guide(request.user):
        messages.error(request, 'Access denied.')
        return redirect('guide_login')

    guide = Guide.objects.get(user=request.user)

    # Get filter parameters
    status_filter = request.GET.get('status')
    date_filter = request.GET.get('date')

    bookings = Booking.objects.filter(guide=guide).order_by('-tour_date__start_date')

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    if date_filter == 'upcoming':
        bookings = bookings.filter(tour_date__start_date__gte=date.today())
    elif date_filter == 'past':
        bookings = bookings.filter(tour_date__end_date__lt=date.today())

    context = {
        'guide': guide,
        'bookings': bookings,
        'current_status_filter': status_filter,
        'current_date_filter': date_filter,
    }

    return render(request, 'guides/guide_bookings.html', context)

@login_required
@csrf_protect
def guide_schedule(request):
    """Guide availability management"""
    if not is_guide(request.user):
        messages.error(request, 'Access denied.')
        return redirect('guide_login')

    guide = Guide.objects.get(user=request.user)

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

        action = "set as available" if is_available else "set as unavailable"
        messages.success(request, f'Date {availability_date} {action}.')
        return redirect('guide_schedule')

    # Get availability for next 60 days
    availability_dates = []
    today = date.today()
    for i in range(60):
        check_date = today + timedelta(days=i)
        try:
            availability = GuideAvailability.objects.get(guide=guide, date=check_date)
            is_available = availability.is_available
        except GuideAvailability.DoesNotExist:
            is_available = True  # Default to available

        # Check if there are bookings on this date
        has_booking = Booking.objects.filter(
            guide=guide,
            tour_date__start_date__lte=check_date,
            tour_date__end_date__gte=check_date,
            status__in=['confirmed', 'pending']
        ).exists()

        availability_dates.append({
            'date': check_date,
            'is_available': is_available,
            'has_booking': has_booking
        })

    return render(request, 'guides/guide_schedule.html', {
        'guide': guide,
        'availability_dates': availability_dates,
        'today': today
    })

@login_required
def guide_feedback(request):
    """View feedback received from customers"""
    if not is_guide(request.user):
        messages.error(request, 'Access denied.')
        return redirect('guide_login')

    guide = Guide.objects.get(user=request.user)

    feedback_list = GuideFeedback.objects.filter(guide=guide).order_by('-created_at').select_related(
        'booking__customer__user',
        'booking__tour_date__tour_package'
    )

    # Calculate statistics
    stats = GuideFeedback.objects.filter(guide=guide).aggregate(
        avg_knowledge=Avg('knowledge_rating'),
        avg_communication=Avg('communication_rating'),
        avg_professionalism=Avg('professionalism_rating'),
        total_count=Count('id')
    )

    # Get monthly feedback trends (last 6 months)
    monthly_stats = []
    for i in range(6):
        month_date = date.today().replace(day=1) - timedelta(days=30 * i)
        month_feedback = GuideFeedback.objects.filter(
            guide=guide,
            created_at__year=month_date.year,
            created_at__month=month_date.month
        )

        month_avg = month_feedback.aggregate(
            avg_overall=Avg('knowledge_rating')  # Can be expanded to include all ratings
        )['avg_overall'] or 0

        monthly_stats.append({
            'month': month_date.strftime('%B %Y'),
            'count': month_feedback.count(),
            'avg_rating': round(month_avg, 1)
        })

    context = {
        'guide': guide,
        'feedback_list': feedback_list,
        'stats': stats,
        'monthly_stats': monthly_stats[::-1],  # Reverse to show oldest to newest
    }

    return render(request, 'guides/guide_feedback.html', context)

@login_required
@csrf_protect
def guide_profile_edit(request):
    """Edit guide profile information"""
    if not is_guide(request.user):
        messages.error(request, 'Access denied.')
        return redirect('guide_login')

    guide = Guide.objects.get(user=request.user)

    if request.method == 'POST':
        # Update user information
        guide.user.first_name = request.POST.get('first_name')
        guide.user.last_name = request.POST.get('last_name')
        guide.user.email = request.POST.get('email')
        guide.user.save()

        # Update guide profile (only certain fields)
        guide.phone = request.POST.get('phone')
        guide.bio = request.POST.get('bio')
        guide.languages = request.POST.get('languages')
        guide.specializations = request.POST.get('specializations')
        guide.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('guide_dashboard')

    return render(request, 'guides/guide_profile_edit.html', {'guide': guide})

def guide_logout(request):
    """Guide logout"""
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('guide_login')