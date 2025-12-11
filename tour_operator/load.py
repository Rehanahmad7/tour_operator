#!/usr/bin/env python3
"""
Complete Sample Data Loader for Tour Operator Website

This script creates a complete set of sample data including:
- Regular customer user
- Guide user with profile
- Tours with multiple images
- Tour dates
- Sample bookings and feedback

Usage: python3 load.py
"""

import os
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tour_operator.settings')
django.setup()

from django.contrib.auth.models import User
from tours.models import TourPackage, TourDate, TourImage
from guides.models import Guide, GuideAvailability
from bookings.models import Customer, Booking, CustomTourRequest
from feedback.models import TourFeedback, GuideFeedback

def clear_existing_data():
    """Clear all existing data to start fresh"""
    print("🗑️ Clearing existing data...")

    # Clear in proper order to avoid foreign key constraints
    # Use try-except to handle missing tables gracefully
    try:
        TourFeedback.objects.all().delete()
    except:
        pass

    try:
        GuideFeedback.objects.all().delete()
    except:
        pass

    try:
        Booking.objects.all().delete()
    except:
        pass

    try:
        CustomTourRequest.objects.all().delete()
    except:
        pass

    try:
        TourImage.objects.all().delete()
    except:
        pass

    try:
        TourDate.objects.all().delete()
    except:
        pass

    try:
        TourPackage.objects.all().delete()
    except:
        pass

    try:
        GuideAvailability.objects.all().delete()
    except:
        pass

    try:
        Guide.objects.all().delete()
    except:
        pass

    try:
        Customer.objects.all().delete()
    except:
        pass

    try:
        User.objects.all().delete()
    except:
        pass

    print("✅ Existing data cleared successfully!")

def create_users():
    """Create sample users"""
    print("👥 Creating users...")

    # Create customer user
    customer_user = User.objects.create_user(
        username='john_customer',
        email='john.customer@example.com',
        first_name='John',
        last_name='Doe',
        password='customer123'
    )

    # Create customer profile
    Customer.objects.create(
        user=customer_user,
        phone='+1-555-0111',
        emergency_contact='Jane Doe',
        emergency_phone='+1-555-0222',
        nationality='American'
    )

    # Create guide user
    guide_user = User.objects.create_user(
        username='sarah_guide',
        email='sarah@guides.com',
        first_name='Sarah',
        last_name='Wilson',
        password='guide123'
    )

    # Create guide profile
    guide = Guide.objects.create(
        user=guide_user,
        phone='+1-555-0222',
        experience_years=12,
        languages='English, Spanish, Hindi, French',
        specializations='Mountain trekking, Cultural tours, Wildlife safari, Photography',
        bio='Passionate adventure guide with over 12 years of experience leading tours across Asia, Africa, and Europe. Specialized in high-altitude trekking, cultural immersion, and wildlife photography. Certified wilderness first aid and mountain rescue.',
        rating=4.9,
        is_available=True
    )

    # Set guide availability for next 60 days
    today = date.today()
    for i in range(60):
        availability_date = today + timedelta(days=i)
        # Make guide unavailable on some random days (weekends)
        is_available = availability_date.weekday() < 5  # Monday=0, Sunday=6

        GuideAvailability.objects.create(
            guide=guide,
            date=availability_date,
            is_available=is_available
        )

    print(f"✅ Created customer: {customer_user.username} (password: customer123)")
    print(f"✅ Created guide: {guide_user.username} (password: guide123)")
    print("ℹ️ Admin access: admin/admin123 (hardcoded in system)")

    return customer_user, guide_user, guide

def create_tours_with_images():
    """Create tours with multiple images"""
    print("🏔️ Creating tours with image galleries...")

    # Himalayan Adventure Trek
    tour1 = TourPackage.objects.create(
        name="Himalayan Adventure Trek",
        description="Experience the breathtaking beauty of the Himalayas with our expert guides. This challenging trek takes you through diverse landscapes, traditional Sherpa villages, and offers stunning mountain views including Everest, Annapurna, and other majestic peaks. Perfect for experienced trekkers seeking an unforgettable adventure.",
        duration=7,
        price=1299.00,
        max_participants=8,
        difficulty='difficult',
        location='Nepal - Annapurna Region',
        included_services='Professional mountain guide, accommodation in tea houses, all meals, trekking permits, porter service, emergency evacuation insurance, airport transfers',
        excluded_services='International flights, travel insurance, personal trekking equipment, alcoholic beverages, tips for guide and porter',
        itinerary='Day 1: Arrive in Kathmandu, equipment check and briefing\nDay 2: Fly to Pokhara, drive to Nayapul, start trekking to Ulleri\nDay 3: Trek through rhododendron forests to Ghorepani\nDay 4: Early morning Poon Hill sunrise, continue to Tadapani\nDay 5: Trek to Chhomrong via beautiful valleys\nDay 6: Reach Annapurna Base Camp (4,130m)\nDay 7: Descend to Bamboo, drive back to Pokhara',
        is_active=True
    )

    # Add Himalayan images
    TourImage.objects.create(
        tour_package=tour1,
        image_url='https://images.unsplash.com/photo-1513936089284-bdbeda5bd041?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=2670',
        caption='Majestic Himalayan peaks at sunrise',
        is_primary=True,
        display_order=0
    )

    TourImage.objects.create(
        tour_package=tour1,
        image_url='https://images.unsplash.com/photo-1761204811048-d8ba714db691?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=2670',
        caption='Traditional mountain village with stunning backdrop',
        is_primary=False,
        display_order=1
    )

    # Cultural Heritage Tour - Rajasthan
    tour2 = TourPackage.objects.create(
        name="Rajasthan Cultural Heritage Tour",
        description="Discover the royal heritage of Rajasthan with visits to magnificent palaces, ancient forts, and vibrant bazaars. This immersive cultural experience showcases traditional Rajasthani art, music, cuisine, and crafts. Perfect for families and culture enthusiasts wanting to experience India's rich history and traditions.",
        duration=4,
        price=599.00,
        max_participants=15,
        difficulty='easy',
        location='Rajasthan, India',
        included_services='Expert cultural guide, accommodation in heritage hotels, breakfast and dinner, private transportation, entrance fees to monuments, traditional Rajasthani cultural show',
        excluded_services='International flights, lunch (to allow local food exploration), personal expenses, alcoholic beverages, tips',
        itinerary='Day 1: Arrive in Jaipur, Pink City tour including City Palace and Hawa Mahal\nDay 2: Amber Fort, elephant ride, local handicraft markets and workshops\nDay 3: Drive to Udaipur, City of Lakes tour including Lake Palace and Jagdish Temple\nDay 4: Rural village experience, traditional cooking class, departure',
        is_active=True
    )

    # Add Rajasthan images
    TourImage.objects.create(
        tour_package=tour2,
        image_url='https://images.unsplash.com/photo-1715168931029-2949161ee406?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=2670',
        caption='Magnificent Rajasthani palace architecture',
        is_primary=True,
        display_order=0
    )

    TourImage.objects.create(
        tour_package=tour2,
        image_url='https://images.unsplash.com/photo-1642412145051-88c8aaf1cf54?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=3750',
        caption='Colorful traditional Rajasthani market',
        is_primary=False,
        display_order=1
    )

    # Masai Mara Safari
    tour3 = TourPackage.objects.create(
        name="Masai Mara Safari Wildlife Experience",
        description="Embark on an unforgettable African safari adventure in Kenya's world-famous Masai Mara National Reserve. Witness the incredible wildlife including the Big Five, experience the Great Migration (seasonal), and immerse yourself in Masai culture. This luxury safari combines thrilling game drives with cultural experiences and comfortable accommodation.",
        duration=5,
        price=2199.00,
        max_participants=6,
        difficulty='moderate',
        location='Kenya - Masai Mara National Reserve',
        included_services='4x4 safari vehicle with pop-up roof, professional safari guide, luxury safari camp accommodation, all meals and beverages, park entrance fees, Masai village visit, airport transfers in Nairobi',
        excluded_services='International flights, visa fees, travel insurance, alcoholic beverages, personal expenses, tips for guide and staff',
        itinerary='Day 1: Nairobi pickup, scenic drive to Masai Mara, afternoon game drive\nDay 2: Full day game drive with picnic lunch in the wilderness\nDay 3: Early morning game drive, afternoon Masai village cultural visit\nDay 4: Final game drive focusing on Big Five, photography session\nDay 5: Morning game drive, return journey to Nairobi',
        is_active=True
    )

    # Add Masai Mara images (Note: The URLs provided seem to be Unsplash photo IDs, converting to proper URLs)
    TourImage.objects.create(
        tour_package=tour3,
        image_url='https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?ixlib=rb-4.1.0&auto=format&fit=crop&q=80&w=2670',
        caption='Masai warriors in traditional attire',
        is_primary=True,
        display_order=0
    )

    TourImage.objects.create(
        tour_package=tour3,
        image_url='https://images.unsplash.com/photo-1547036967-23d11aacaee0?ixlib=rb-4.1.0&auto=format&fit=crop&q=80&w=2670',
        caption='African savanna landscape with acacia trees',
        is_primary=False,
        display_order=1
    )

    print(f"✅ Created tour: {tour1.name} with {tour1.images.count()} images")
    print(f"✅ Created tour: {tour2.name} with {tour2.images.count()} images")
    print(f"✅ Created tour: {tour3.name} with {tour3.images.count()} images")

    return [tour1, tour2, tour3]

def create_tour_dates(tours):
    """Create tour dates for each tour"""
    print("📅 Creating tour dates...")

    today = date.today()
    dates_created = 0

    for i, tour in enumerate(tours):
        # Create 4 different date options for each tour
        for j in range(4):
            start_date = today + timedelta(days=30 + (j * 21) + (i * 7))
            end_date = start_date + timedelta(days=tour.duration - 1)

            TourDate.objects.create(
                tour_package=tour,
                start_date=start_date,
                end_date=end_date,
                available_spots=tour.max_participants,
                is_available=True
            )
            dates_created += 1

    print(f"✅ Created {dates_created} tour dates across all tours")

def create_sample_bookings(customer_user, guide, tours):
    """Create sample bookings and feedback"""
    print("📝 Creating sample bookings and feedback...")

    customer = Customer.objects.get(user=customer_user)

    # Create a completed booking with feedback
    past_date = TourDate.objects.filter(tour_package=tours[0]).first()
    if past_date:
        # Simulate a completed tour
        past_date.start_date = date.today() - timedelta(days=30)
        past_date.end_date = date.today() - timedelta(days=24)
        past_date.save()

        booking = Booking.objects.create(
            customer=customer,
            tour_date=past_date,
            guide=guide,
            participants=2,
            total_price=float(past_date.tour_package.price) * 2,
            status='completed',
            booking_date=date.today() - timedelta(days=35)
        )

        # Create tour feedback
        TourFeedback.objects.create(
            booking=booking,
            overall_rating=5,
            guide_rating=5,
            accommodation_rating=4,
            value_for_money_rating=4,
            comments='Absolutely incredible experience! The Himalayan trek was challenging but rewarding. Our guide Sarah was exceptional - knowledgeable, safety-conscious, and great company. The views were breathtaking and the local villages we visited were fascinating. Highly recommend this adventure!',
            would_recommend=True,
            suggestions='Perhaps add more cultural interaction opportunities with local communities.'
        )

        # Create guide feedback
        GuideFeedback.objects.create(
            booking=booking,
            guide=guide,
            knowledge_rating=5,
            communication_rating=5,
            professionalism_rating=5,
            comments='Sarah is an outstanding guide! Her knowledge of the mountains and local culture made the trip educational and engaging. She ensured our safety at all times and was always cheerful and encouraging. We felt completely confident in her abilities.'
        )

    # Create a confirmed upcoming booking
    upcoming_date = TourDate.objects.filter(tour_package=tours[1]).first()
    if upcoming_date:
        Booking.objects.create(
            customer=customer,
            tour_date=upcoming_date,
            guide=guide,
            participants=3,
            total_price=float(upcoming_date.tour_package.price) * 3,
            status='confirmed',
            booking_date=date.today() - timedelta(days=5)
        )

    # Create a custom tour request
    CustomTourRequest.objects.create(
        customer=customer,
        destination='Bhutan Dragon Kingdom',
        duration=10,
        preferred_dates=f'{date.today() + timedelta(days=90)} to {date.today() + timedelta(days=100)}',
        participants=4,
        budget_range='3000-4000',
        special_requirements='High-altitude trekking experience, photography focus, monastery visits, vegetarian meals only'
    )

    print("✅ Created sample bookings and feedback")
    print("✅ Created custom tour request")

def create_sample_data():
    """Main function to create all sample data"""
    print("🚀 Starting Tour Operator Sample Data Creation...")
    print("=" * 60)

    # Only clear if there are existing users
    if User.objects.exists():
        print("🗑️ Found existing data, clearing first...")
        clear_existing_data()
    else:
        print("📝 Fresh database detected, creating sample data...")

    # Create users
    customer_user, guide_user, guide = create_users()

    # Create tours with images
    tours = create_tours_with_images()

    # Create tour dates
    create_tour_dates(tours)

    # Create sample bookings and feedback
    create_sample_bookings(customer_user, guide, tours)

    print("=" * 60)
    print("🎉 SAMPLE DATA CREATION COMPLETE!")
    print("=" * 60)
    print()
    print("🔑 LOGIN CREDENTIALS:")
    print("------------------------")
    print("👤 Customer Login:")
    print("   Username: john_customer")
    print("   Password: customer123")
    print()
    print("🧭 Guide Login:")
    print("   Username: sarah_guide")
    print("   Password: guide123")
    print()
    print("🔧 Admin Login (Hardcoded):")
    print("   Username: admin")
    print("   Password: admin123")
    print()
    print("🌐 ACCESS URLS:")
    print("------------------------")
    print("🏠 Main Website: http://127.0.0.1:8000")
    print("🧭 Guide Portal: http://127.0.0.1:8000/guides/login/")
    print("🔧 Admin Dashboard: http://127.0.0.1:8000/tour-admin/")
    print("⚙️ Django Admin: http://127.0.0.1:8000/admin/")
    print()
    print("📊 SAMPLE DATA SUMMARY:")
    print("------------------------")
    print(f"👥 Users: 2 (1 customer, 1 guide)")
    print(f"🏔️ Tours: {len(tours)} (with image galleries)")
    print(f"📅 Tour Dates: {TourDate.objects.count()}")
    print(f"🖼️ Images: {TourImage.objects.count()}")
    print(f"📝 Bookings: {Booking.objects.count()}")
    print(f"⭐ Feedback: {TourFeedback.objects.count() + GuideFeedback.objects.count()}")
    print()
    print("🚀 READY TO START:")
    print("Run: python3 manage.py runserver")
    print("Visit: http://127.0.0.1:8000")

if __name__ == '__main__':
    create_sample_data()