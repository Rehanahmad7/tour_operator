# Tour Operator Website

A comprehensive Django-based tour operator website with package management, booking handling, guide assignment, customer feedback collection, and advanced image galleries.

## 🌟 Features

### Core Functionality
- **Tour Package Management**: Create and manage tour packages with detailed information and multiple images
- **Dynamic Booking System**: Real-time booking with availability tracking
- **Guide Assignment**: Assign experienced guides to tours with availability management
- **Customer Feedback**: Comprehensive feedback and rating system
- **Custom Tour Planning**: Allow customers to request personalized tours
- **Image Gallery System**: Multiple images per tour with primary image selection

### 👥 User Features
- User authentication and session management
- Tour browsing with image galleries
- Detailed tour views with interactive image galleries
- Online booking with participant management
- Booking history and status tracking
- Feedback submission for completed tours
- Custom tour request submission

### 🔧 Admin Features
- **Hardcoded Admin System**: Direct admin access with credentials (admin/admin123)
- Complete tour management with multi-image support
- Dynamic image input system with real-time previews
- Booking management and guide assignment
- Customer and guide profile management
- Feedback monitoring and analysis
- Custom tour request processing
- Guide performance dashboard

### 🧭 Guide Features
- **Dedicated Guide Dashboard**: Comprehensive portal for guides
- Guide authentication and login system
- Tour and booking management interface
- 60-day availability calendar with visual indicators
- Performance feedback viewing with statistics
- Profile editing capabilities
- Earnings and statistics overview

### 🖼️ Image Management
- **Multiple Images per Tour**: Add unlimited images with URLs
- **Primary Image Selection**: Set featured images for tours
- **Interactive Galleries**: Click-through image galleries on tour pages
- **Real-time Previews**: See images as you add URLs in admin
- **Responsive Design**: Image galleries work on all devices
- **Fallback Placeholders**: Beautiful gradients when no images exist

## 🛠️ Technology Stack

- **Backend**: Django 4.2.25
- **Database**: SQLite (with custom TourImage model)
- **Frontend**: Bootstrap 5.1.3 + Custom CSS/JavaScript
- **Authentication**: Django's built-in auth + Custom guide authentication
- **Image Handling**: URL-based with validation and previews

## 🚀 Quick Start Guide

### **🎯 One-Command Setup (Easiest)**

For instant setup with everything included:

```bash
cd tour_operator
pip install Django  # if not installed
python3 setup.py
python3 manage.py runserver
```

Then visit: **http://127.0.0.1:8000** 🎉

### **📋 Manual Setup (Step by Step)**

If you prefer manual control:

1. **Navigate to project directory**:
   ```bash
   cd tour_operator
   ```

2. **Install Django** (if not already installed):
   ```bash
   pip install Django
   ```

3. **Run migrations**:
   ```bash
   python3 manage.py migrate
   ```

4. **Load complete sample data** (users, tours, images, bookings):
   ```bash
   python3 load.py
   ```

5. **Start the server**:
   ```bash
   python3 manage.py runserver
   ```

6. **Access the application**:
   - **🏠 Main Website**: http://127.0.0.1:8000
   - **🧭 Guide Portal**: http://127.0.0.1:8000/guides/login/
   - **🔧 Admin Dashboard**: http://127.0.0.1:8000/tour-admin/
   - **⚙️ Django Admin**: http://127.0.0.1:8000/admin

### **🔑 Default Login Credentials**

After running the load script, use these credentials:

**👤 Customer Account:**
- Username: `john_customer`
- Password: `customer123`

**🧭 Guide Account:**
- Username: `sarah_guide`
- Password: `guide123`

**🔧 Admin Account (Hardcoded):**
- Username: `admin`
- Password: `admin123`

### **Alternative Setup (Manual)**

If you prefer manual setup:

1. **Run migrations only**:
   ```bash
   python3 manage.py migrate
   ```

2. **Create superuser** (optional):
   ```bash
   python3 manage.py createsuperuser
   ```

3. **Start server**:
   ```bash
   python3 manage.py runserver
   ```

## 📁 Project Structure

```
tour_operator/
├── tour_operator/          # Project settings and admin views
├── tours/                  # Tour package and image management
├── bookings/              # Booking and customer management
├── guides/                # Guide management and dashboard
├── feedback/              # Feedback and rating system
├── templates/             # HTML templates
│   ├── admin/            # Custom admin templates
│   ├── guides/           # Guide dashboard templates
│   └── tours/            # Public tour templates
├── load_sample_data.py    # Sample data loader
└── manage.py              # Django management script
```

## 🗄️ Models Overview

### Tours App
- **TourPackage**: Tour details, pricing, difficulty, location with image relationships
- **TourDate**: Available dates for each tour package
- **TourImage**: Multiple images per tour with primary selection and display order

### Guides App
- **Guide**: Guide profiles with experience, ratings, and specializations
- **GuideAvailability**: Track guide availability by date

### Bookings App
- **Customer**: Customer profiles linked to Django users
- **Booking**: Tour bookings with status tracking and guide assignment
- **CustomTourRequest**: Custom tour requests from customers

### Feedback App
- **TourFeedback**: Overall tour experience ratings
- **GuideFeedback**: Specific guide performance ratings with detailed metrics

## 🔑 Key Features Implementation

### 🎯 Admin Dashboard
- **Hardcoded Authentication**: Secure admin access without Django admin
- **Tour Management**: Create/edit tours with dynamic image inputs
- **Image Gallery Management**: Add multiple images with captions and primary selection
- **Guide Management**: Create and manage guide profiles
- **Statistics Dashboard**: Comprehensive overview of bookings, tours, and performance

### 🧭 Guide Portal
- **Authentication System**: Role-based access for guides
- **Performance Dashboard**: Statistics, earnings, and recent activity
- **Booking Management**: View and manage assigned tours
- **Availability Calendar**: 60-day visual calendar for availability management
- **Feedback Viewing**: See customer feedback with rating breakdowns
- **Profile Management**: Edit personal and professional information

### 🖼️ Image Gallery System
- **Dynamic Admin Interface**: Add/remove images with JavaScript
- **Primary Image Selection**: Radio button selection for featured images
- **Interactive Galleries**: Click-to-switch main image on tour details
- **Responsive Design**: Mobile-friendly image displays
- **Visual Feedback**: Active thumbnail highlighting

### 🔒 Authentication & Security
- **Multi-tier Authentication**: Customer, Guide, and Admin systems
- **CSRF Protection**: Enhanced form security across all interfaces
- **Session Management**: Proper user state handling
- **Role-based Access**: Different interfaces for different user types

### 📱 Responsive Design
- **Mobile-first**: Bootstrap 5 responsive framework
- **Custom CSS**: Beautiful gradients and modern styling
- **Interactive Elements**: JavaScript-enhanced user experience
- **Cross-device Compatibility**: Works on phones, tablets, and desktop

## 📋 Usage Guide

### 🎫 Booking a Tour (Customer)
1. Browse tours with image galleries
2. View detailed tour information and photo galleries
3. Login or register as a customer
4. Select dates and participants
5. Submit booking and receive guide assignment

### 🧭 Guide Dashboard
1. **Login**: Navigate to `/guides/login/`
2. **Credentials**: Use guide credentials from sample data
3. **Dashboard**: View statistics, upcoming tours, and recent bookings
4. **Manage Schedule**: Set availability for next 60 days
5. **View Feedback**: See customer ratings and comments
6. **Edit Profile**: Update personal and professional information

### 🔧 Admin Management
1. **Access**: Go to `/tour-admin/` (admin/admin123)
2. **Create Tours**: Add tours with multiple images
3. **Manage Images**: Upload images with captions and set primary
4. **Assign Guides**: Connect guides to bookings
5. **Monitor Performance**: View dashboard statistics

### 🖼️ Image Management
1. **Add Images**: Use "Add Another Image" button
2. **Set Primary**: Select radio button for featured image
3. **Preview**: See image previews as you add URLs
4. **Gallery View**: Click thumbnails to switch main image

## 📊 Sample Data

The `load.py` script creates comprehensive sample data including:

### **🧑‍💼 Users & Accounts**
- **Customer**: john_customer (complete profile with bookings)
- **Guide**: sarah_guide (professional profile with 12 years experience)
- **Admin**: Hardcoded admin access (admin/admin123)

### **🏔️ Tours with Image Galleries**
1. **Himalayan Adventure Trek** (₹1,299)
   - 7-day challenging trek in Nepal
   - 2 high-quality Unsplash images
   - Mountain peaks and traditional villages

2. **Rajasthan Cultural Heritage Tour** (₹599)
   - 4-day cultural immersion
   - 2 beautiful palace and market images
   - Easy difficulty for families

3. **Masai Mara Safari Wildlife Experience** (₹2,199)
   - 5-day luxury African safari
   - 2 stunning wildlife and landscape images
   - Moderate difficulty adventure

### **📅 Booking Scenarios**
- **Completed Tour**: Past Himalayan trek with 5-star feedback
- **Upcoming Booking**: Confirmed Rajasthan tour
- **Custom Request**: Bhutan trekking inquiry
- **Guide Availability**: 60-day calendar with realistic schedule

### **⭐ Feedback & Reviews**
- Detailed customer tour feedback with ratings
- Comprehensive guide performance reviews
- Realistic comments and rating distributions
- Complete feedback system demonstration

## 🎨 Design Features

### Visual Elements
- **Modern UI**: Clean, professional interface design
- **Color Scheme**: Professional blues and gradients
- **Icons**: Font Awesome integration for visual cues
- **Cards**: Bootstrap card components for organized layout

### User Experience
- **Intuitive Navigation**: Clear menu structure across all interfaces
- **Visual Feedback**: Loading states, hover effects, and active states
- **Error Handling**: Graceful error messages and validation
- **Responsive Images**: Optimized display across all screen sizes

## 🚀 Development Highlights

This project demonstrates:
- **Advanced Django Architecture**: Multi-app structure with custom admin
- **Database Design**: Complex relationships with image handling
- **Frontend Integration**: JavaScript + CSS + Django templates
- **User Experience**: Multi-role interfaces with distinct workflows
- **Image Management**: URL-based system with validation
- **Security Implementation**: CSRF protection and authentication
- **Responsive Development**: Mobile-first design principles

## 💡 Advanced Features

### Image Gallery System
- **Unlimited Images**: Add as many images as needed per tour
- **Smart Ordering**: Display order management
- **Primary Selection**: Automatic primary image enforcement
- **Interactive Viewing**: Click-through galleries with active states
- **Fallback Handling**: Beautiful placeholders for missing images

### Guide Dashboard
- **Comprehensive Analytics**: Earnings, ratings, and tour statistics
- **Visual Calendar**: 60-day availability with color-coded states
- **Performance Tracking**: Customer feedback with rating breakdowns
- **Profile Management**: Self-service profile editing

### Admin Efficiency
- **Hardcoded Access**: No need for Django superuser creation
- **Bulk Operations**: Manage multiple images simultaneously
- **Real-time Feedback**: Instant previews and validation
- **Comprehensive Management**: All aspects controllable from one interface

## 🔄 Future Enhancements

### Immediate Opportunities
- **File Upload**: Replace URL system with file upload
- **Image Optimization**: Automatic resizing and compression
- **Bulk Image Management**: Upload multiple images at once
- **Advanced Gallery**: Lightbox modals and zoom functionality

### Long-term Features
- **Payment Integration**: Stripe/PayPal integration
- **Email Notifications**: Automated booking confirmations
- **Mobile App API**: REST API for mobile applications
- **Advanced Analytics**: Detailed reporting and insights
- **Multi-language Support**: Internationalization
- **Social Integration**: Social media sharing and reviews
- **Weather API**: Real-time weather for tour locations
- **GPS Integration**: Location-based features

## 🏆 Project Achievements

- ✅ **Complete CRUD Operations** across all entities
- ✅ **Multi-role Authentication** (Customer, Guide, Admin)
- ✅ **Advanced Image Management** with galleries
- ✅ **Responsive Design** across all interfaces
- ✅ **Real-time Interactions** with JavaScript
- ✅ **Comprehensive Dashboard** systems
- ✅ **Security Implementation** with CSRF protection
- ✅ **Professional UI/UX** with modern design principles

This tour operator website showcases modern web development practices with Django, providing a complete business solution with beautiful image galleries, comprehensive management interfaces, and excellent user experience across all user roles.
