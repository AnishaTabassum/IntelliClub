from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import Clubs, ClubsEvents, Users, Students,Clubs, ClubsMembers, Events,EventRegistration, ClubsRegistration
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Login error
            messages.error(request, "Invalid email or password.")
            return render(request, 'dashboard/login.html')
            
    # Regular GET request (initial page load)
    return render(request, 'dashboard/login.html')

def register_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        
        # 1. Check if the Student_ID already exists
        if Students.objects.filter(student_id=student_id).exists():
            messages.error(request, f"Student ID {student_id} is already registered.")
            return render(request, 'dashboard/login.html', {'show_register_modal': True}) # Stay on page

        # 2. Check if the Email already exists (Optional but recommended)
        if Students.objects.filter(email=email).exists():
            messages.error(request, "This email is already associated with an account.")
            return render(request, 'dashboard/login.html', {'show_register_modal': True}) # Stay on page
        
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
    # 1. Get all clubs for the main browse table
    clubs = Clubs.objects.all()
    
    try:
        # 2. Identify the SPECIFIC student logged in
        # We use request.user.user_email to match your custom User model
        student = Students.objects.get(email=request.user.user_email)
        
        # 3. CRITICAL: Filter memberships ONLY for this student
        # If you use .all() here, EVERYONE sees EVERYONE'S clubs in the sidebar!
        my_clubs = ClubsMembers.objects.filter(student=student)
        
        # 4. Get lists for the badges on the main table
        joined_club_ids = list(my_clubs.values_list('club_id', flat=True))
        pending_club_ids = list(ClubsRegistration.objects.filter(student=student).values_list('club_id', flat=True))
        
    except Students.DoesNotExist:
        # If the student record isn't found, the sidebar should be empty
        my_clubs = []
        joined_club_ids = []
        pending_club_ids = []

    return render(request, 'dashboard/all_clubs.html', {
        'clubs': clubs,
        'my_clubs': my_clubs, # This now only contains Labib's data
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
    # 1. Standard setup
    student = Students.objects.get(email=request.user.user_email)
    club = get_object_or_404(Clubs, club_id=club_id)
    membership = get_object_or_404(ClubsMembers, student=student, club=club)
    
    # 2. Fix the FieldError: Get events linked to this club via the bridge table
    # We filter ClubsEvents by the club_id string in your model
    event_links = ClubsEvents.objects.filter(club_id=club.club_id).select_related('event')
    
    # 3. Extract the actual 'Events' objects for the template
    club_events = [link.event for link in event_links]
    
    all_members = ClubsMembers.objects.filter(club=club).select_related('student')

    context = {
        'club': club,
        'all_members': all_members,
        'club_events': club_events, 
        'role': membership.role,
    }

    # 4. Redirect based on Executive vs Member
    if membership.role in ['President', 'Vice President', 'Executive']:
        context['pending_requests'] = ClubsRegistration.objects.filter(club=club)
        return render(request, 'dashboard/exec_dashboard.html', context)
    else:
        # Ensure this file is saved in templates/dashboard/member_view.html
        return render(request, 'dashboard/members_view.html', context)
    
@login_required
def approve_member(request, reg_id):
    if request.method == 'POST':
        pending = get_object_or_404(ClubsRegistration, reg_id=reg_id)
        club_id = pending.club.club_id
        
        with transaction.atomic():
            # Create the membership record
            ClubsMembers.objects.create(
                student=pending.student,
                club=pending.club,
                role='General Member'
            )
            # Remove from pending list
            pending.delete()
            
        messages.success(request, f"Approved {pending.student.email} successfully!")
        return redirect('club_dashboard', club_id=club_id)
    
@login_required
def reject_member(request, reg_id):
    if request.method == 'POST':
        pending = get_object_or_404(ClubsRegistration, reg_id=reg_id)
        club_id = pending.club.club_id
        
        # Simply delete the registration request
        pending.delete()
        
        messages.warning(request, "Membership request rejected.")
        return redirect('club_dashboard', club_id=club_id)

@login_required
def toggle_registration(request, club_id):
    if request.method == "POST":
        # 1. Get the club
        club = get_object_or_404(Clubs, club_id=club_id)
        
        # 2. Security Check: Ensure the user is an executive of THIS club
        is_exec = ClubsMembers.objects.filter(
            student__email=request.user.user_email, 
            club=club, 
            role__in=['President', 'Vice President', 'Secretary', 'Treasurer']
        ).exists()

        if is_exec:
            club.reg_open = not club.reg_open  # Flip the 1 to 0 or 0 to 1
            club.save()
            status = "Open" if club.reg_open else "Closed"
            messages.success(request, f"Registration is now {status} for {club.club_name}.")
        else:
            messages.error(request, "You do not have permission to change this setting.")
            
    return redirect('club_dashboard', club_id=club_id)