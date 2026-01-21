from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import Clubs, Users, Students,Clubs, ClubsMembers, Events,EventRegistration, ClubsRegistration
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    # Fetch events
    upcoming_focus_events = Events.objects.all().order_by('event_date')[:3]
    
    try:
        current_student = Students.objects.get(email=request.user.user_email)
        # Fetch memberships - Django now uses Member_ID behind the scenes
        my_clubs = ClubsMembers.objects.filter(student=current_student)
        
        # Registration logic
        registrations = EventRegistration.objects.filter(student=current_student)
        registered_list = [reg.event for reg in registrations]
    except Students.DoesNotExist:
        my_clubs = []
        registered_list = []

    context = {
        'events': upcoming_focus_events,
        'my_events': registered_list,
        'my_clubs': my_clubs,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def all_clubs_view(request):
    # 1. Fetch all clubs for the main table
    clubs = Clubs.objects.all()
    
    try:
        # 2. Connect User to Student using the email
        student = Students.objects.get(email=request.user.user_email)
        
        # 3. Data for Sidebar (Active memberships)
        my_clubs = ClubsMembers.objects.filter(student=student)
        
        # 4. Get IDs of clubs already joined (for "Member" badge)
        joined_club_ids = list(my_clubs.values_list('club_id', flat=True))
        
        # 5. Get IDs of clubs with pending requests (for "Requested" badge)
        # We use payment_status='Unpaid' to represent a pending state in your schema
        pending_club_ids = list(ClubsRegistration.objects.filter(
            student=student
        ).values_list('club_id', flat=True))
        
    except Students.DoesNotExist:
        my_clubs = []
        joined_club_ids = []
        pending_club_ids = []

    return render(request, 'dashboard/all_clubs.html', {
        'clubs': clubs,
        'my_clubs': my_clubs, # For sidebar
        'joined_club_ids': joined_club_ids,
        'pending_club_ids': pending_club_ids,
    })

@login_required
def join_club_request(request, club_id):
    try:
        # 1. Get student and club using the new ID names
        student = Students.objects.get(email=request.user.user_email)
        club = Clubs.objects.get(club_id=club_id)

        # 2. Check if already a member
        if ClubsMembers.objects.filter(student=student, club=club).exists():
            messages.info(request, "You are already a member of this club.")
            return redirect('all_clubs')

        # 3. Check if a request is already pending (using reg_id logic)
        if ClubsRegistration.objects.filter(student=student, club=club).exists():
            messages.warning(request, "Your membership request is already pending.")
            return redirect('all_clubs')

        # 4. Create the Request using your SQL field: 'payment_status'
        # Since your SQL doesn't have a 'status' column, we use 'Unpaid' as the pending state
        ClubsRegistration.objects.create(
            student=student,
            club=club,
            payment_status='Unpaid' 
        )
        
        messages.success(request, f"Request sent to {club.club_name}!")

    except Students.DoesNotExist:
        messages.error(request, "Student record not found.")
    
    return redirect('all_clubs')

@login_required
def club_dashboard_view(request, club_id):
    student = Students.objects.get(email=request.user.user_email)
    club = Clubs.objects.get(club_id=club_id)
    
    # Fetch membership
    membership = get_object_or_404(ClubsMembers, student=student, club=club)
    
    # Check for Admin/Executive roles (matching your sidebar logic)
    if membership.role != 'General Member':
        # Fetch pending requests where payment_status is 'Unpaid'
        pending_requests = ClubsRegistration.objects.filter(club=club, payment_status='Unpaid')
        return render(request, 'dashboard/exec_dashboard.html', {
            'club': club,
            'pending_requests': pending_requests,
            'role': membership.role
        })
    else:
        return render(request, 'dashboard/member_view.html', {
            'club': club,
            'role': membership.role
        })
    
@login_required
def approve_member(request, reg_id): # Changed to match your SQL 'reg_id'
    if request.method == 'POST':
        try:
            pending = ClubsRegistration.objects.get(reg_id=reg_id)
            club_id = pending.club.club_id
            
            with transaction.atomic():
                # Move to ClubsMembers
                ClubsMembers.objects.create(
                    student=pending.student,
                    club=pending.club,
                    role='General Member'
                )
                # Delete the registration record
                pending.delete()
                
            messages.success(request, "Member approved!")
            return redirect('club_dashboard', club_id=club_id)
            
        except ClubsRegistration.DoesNotExist:
            messages.error(request, "Request not found.")
            
    return redirect('home')