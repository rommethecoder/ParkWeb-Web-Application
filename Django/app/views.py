from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from app.models import *
from datetime import datetime
from django import forms
from django.forms import DateTimeInput
from django.contrib.auth.decorators import user_passes_test


def homePage(request):
    context = {}
    return render(request, "home.html", context)


def about(request):
    context = {}
    return render(request, "about.html", context)


def map_calendarPage(request):
    area = Area.objects.all()
    event = Event.objects.all()
    booking = Booking.objects.all()

    bookableArea = Area.objects.raw(
        """
            SELECT * FROM area
            WHERE area.id NOT IN (
                SELECT booking.area_id
                FROM booking
            )
        """
    )

    categories = [
        "Tech",
        "Music",
        "Sports",
        "Recreation",
        "Super Mega Fun",
    ]

    context = {
        "areas": area,
        "events": event,
        "bookings": booking,
        "bookableAreas": bookableArea,
        "current_date": datetime.now(),
        "eventCategories": categories,
    }

    return render(request, "map_calendar.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'username/password is incorrect !')

    context = {}
    return render(request, "login.html", context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was successfully created for ' + username)
                return redirect('login')

    context = {'form': form}
    return render(request, "register.html", context)


def create_event_and_booking(request):
    if request.method == 'POST':
        # Extract data from the form
        event_name = request.POST.get('event_name')
        event_date_str = request.POST.get('event_date')
        is_public = request.POST.get('is_public') == 'true'
        event_category = request.POST.get('event_category')
        event_description = request.POST.get('event_description')
        estimated_attendance = request.POST.get('attendance')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        area_id = request.POST.get('area_id')
        user_id = request.user.id  # Assuming the user is logged in

        # Convert date and time strings to datetime objects
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()

        # Combine date and time to create datetime objects
        event_start_datetime = datetime.combine(event_date, start_time)
        event_end_datetime = datetime.combine(event_date, end_time)

        # Create Event object
        event = Event.objects.create(
            name=event_name,
            date=event_start_datetime,
            is_public=is_public,
            category=event_category,
            description=event_description
        )

        # Create Booking object
        booking = Booking.objects.create(
            start_time=event_start_datetime,
            end_time=event_end_datetime,
            attendance=estimated_attendance,
            area_id=area_id,
            event_id=event.id,
            user_id=user_id
        )

        # Return success response
        return redirect('map_calendar')
    else:
        return redirect('map_calendar')


def logoutUser(request):
    logout(request)
    return redirect('home')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'is_public', 'category', 'description']

    # Add a DateTimeInput widget for the EventDate field
    date = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        help_text='Format: YYYY-MM-DD HH:MM',
    )


def get_events(request):
    # Filter events based on approved bookings
    approved_bookings = Booking.objects.filter(status='Approved')

    event_data = []

    for booking in approved_bookings:
        if booking.event.is_public:
            event_title = booking.event.name
        else:
            event_title = "Private Event"
        event_data.append({
            'id': booking.event.id,
            'title': event_title,
            'date': booking.event.date,
            'startTime': booking.start_time,
            'endTime': booking.end_time,
            'category': booking.event.category,
            'description': booking.event.description,
        })

    return JsonResponse(event_data, safe=False)


def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings_list.html', {'bookings': bookings})
