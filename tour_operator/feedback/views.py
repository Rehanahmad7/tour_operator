from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TourFeedback, GuideFeedback
from bookings.models import Booking
from .forms import TourFeedbackForm, GuideFeedbackForm

@login_required
def submit_feedback(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer__user=request.user, status='completed')

    if TourFeedback.objects.filter(booking=booking).exists():
        messages.info(request, 'You have already submitted feedback for this tour.')
        return redirect('my_bookings')

    if request.method == 'POST':
        tour_form = TourFeedbackForm(request.POST)
        guide_form = GuideFeedbackForm(request.POST) if booking.guide else None

        if tour_form.is_valid() and (not guide_form or guide_form.is_valid()):
            tour_feedback = tour_form.save(commit=False)
            tour_feedback.booking = booking
            tour_feedback.save()

            if guide_form and booking.guide:
                guide_feedback = guide_form.save(commit=False)
                guide_feedback.guide = booking.guide
                guide_feedback.booking = booking
                guide_feedback.save()

            messages.success(request, 'Thank you for your feedback!')
            return redirect('my_bookings')
    else:
        tour_form = TourFeedbackForm()
        guide_form = GuideFeedbackForm() if booking.guide else None

    return render(request, 'feedback/submit_feedback.html', {
        'tour_form': tour_form,
        'guide_form': guide_form,
        'booking': booking
    })

def feedback_list(request):
    tour_feedbacks = TourFeedback.objects.all().order_by('-created_at')[:10]
    return render(request, 'feedback/feedback_list.html', {'feedbacks': tour_feedbacks})
