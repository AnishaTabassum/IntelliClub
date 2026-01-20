from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import Clubs, Users, Students,Clubs, ClubsMembers, Events
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')

        # authenticate looks at dashboard.Users because of our settings
        user = authenticate(request, username=email_input, password=password_input)

        if user is not None:
            login(request, user)
            return redirect('home') # We'll create this later
        else:
            return render(request, 'dashboard/login.html', {'error': 'Invalid email or password.'})

    return render(request, 'dashboard/login.html')

def register_view(request):
    if request.method == "POST":
        # Get data from form
        sid = request.POST.get('student_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        pw = request.POST.get('password')
        dept = request.POST.get('department')
        ptype = request.POST.get('personality')

        try:
            with transaction.atomic(): # Ensures both save or none save
                # 1. Create User (Hashed)
                new_user = Users(user_email=email)
                new_user.set_password(pw)
                new_user.save()

                # 2. Create Student profile linked to User
                new_student = Students(
                    student_id=sid,
                    name=name,
                    email=new_user, # Foreign Key link
                    department=dept,
                    personality_type=ptype
                )
                new_student.save()

            return redirect('login') # Success!
        except Exception as e:
            return render(request, 'dashboard/login.html', {'error': f'Registration failed: {e}'})
        
@login_required
def home_view(request):
    # 1. Fetch Events from DB
    raw_events = Events.objects.all().order_by('event_date')[:3]
    
    icon_map = {
        'Workshop': 'bi-mortarboard',
        'Competition': 'bi-trophy',
        'Talk': 'bi-megaphone',
        'Seminar': 'bi-lightbulb',
    }

    for event in raw_events:
        event.display_icon = icon_map.get(event.event_type, 'bi-star')

    # 2. FIX: Connect User to Student using the 'email' field
    try:
        # Based on your error, the field is 'email', not 'student_email'
        current_student = Students.objects.get(email=request.user.user_email)
        my_clubs = ClubsMembers.objects.filter(student=current_student)
    except Students.DoesNotExist:
        my_clubs = []

    context = {
        'events': raw_events,
        'my_clubs': my_clubs,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def all_clubs_view(request):
    # 1. Fetch all clubs for the main table
    clubs = Clubs.objects.all()
    
    # 2. FIX: Connect User to Student for the sidebar
    try:
        # Use 'email' as identified in your previous FieldError
        current_student = Students.objects.get(email=request.user.user_email)
        my_clubs = ClubsMembers.objects.filter(student=current_student)
    except Students.DoesNotExist:
        my_clubs = []

    return render(request, 'dashboard/all_clubs.html', {
        'clubs': clubs,
        'my_clubs': my_clubs
    })