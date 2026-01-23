from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.db.models import Q,Count
from .models import Clubs, ClubsEvents, Users, Students,Clubs, ClubsMembers, Events,EventRegistration, ClubsRegistration, Volunteers
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

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
    # Fetch top 3 events for the cards
    upcoming_focus_events = Events.objects.all().order_by('event_date')[:3]
    
    try:
        current_student = Students.objects.get(email=request.user.user_email)
        
        # Sidebar data
        my_clubs = ClubsMembers.objects.filter(student=current_student).select_related('club')
        
        # Optimized registration logic for the "My Registered Events" table
        # We fetch the registrations and the linked event data in one go
        registrations = EventRegistration.objects.filter(student=current_student).select_related('event')
        
    except Students.DoesNotExist:
        my_clubs = []
        registrations = []

    context = {
        'events': upcoming_focus_events,
        'my_registrations': registrations, # Use registrations to access both Event and Reg data
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
        my_clubs = ClubsMembers.objects.filter(student=student).select_related('club')
        
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
    my_clubs = ClubsMembers.objects.filter(student=student).select_related('club')
    
    # 2. Get events linked to this club
    event_links = ClubsEvents.objects.filter(club_id=club.club_id).select_related('event')
    club_events = [link.event for link in event_links]
    
    # Get IDs of these events to filter registrations
    club_event_ids = [link.event.event_id for link in event_links]
    
    all_members = ClubsMembers.objects.filter(club=club).select_related('student')

    context = {
        'club': club,
        'my_clubs': my_clubs,
        'all_members': all_members,
        'club_events': club_events, 
        'role': membership.role,
    }

    # 4. Executive Specific Logic
    if membership.role in ['President', 'Vice President', 'Executive']:
        # Club Membership Requests (already there)
        context['pending_requests'] = ClubsRegistration.objects.filter(club=club)
        
        # NEW: Event Registration Requests
        # We filter for 'Unpaid' status which represents a new request
        context['event_reg_requests'] = EventRegistration.objects.filter(
            event_id__in=club_event_ids, 
            payment_status='Unpaid'
        ).select_related('student', 'event')
        
        return render(request, 'dashboard/exec_dashboard.html', context)
    else:
        return render(request, 'dashboard/members_view.html', context)
    
@login_required
def approve_event_registration(request, registration_id):
    registration = get_object_or_404(EventRegistration, registration_id=registration_id)
    
    if request.method == "POST":
        # Use 'Success' to match your MySQL ENUM exactly
        registration.payment_status = 'Success'
        registration.save()
        
    # FIX: Redirect to 'club_dashboard', not 'club_event_manager'
    return redirect('club_dashboard', club_id=registration.event.club_id)
    
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

def create_event_page(request, club_id):
    hosting_club = get_object_or_404(Clubs, club_id=club_id)
    
    if request.method == "POST":
        # 1. Capture Form Data
        name = request.POST.get('event_name')
        date_str = request.POST.get('event_date')
        time_str = request.POST.get('event_time')
        venue = request.POST.get('venue')
        details = request.POST.get('details')
        event_type = request.POST.get('event_type')
        fee = request.POST.get('event_fee') or 0
        
        # Combine Date and Time for DateTimeField
        full_datetime = None
        if date_str and time_str:
            full_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

        # 2. Handle Budgets and Partners
        # Get all budget shares (host is usually the first one)
        shares = request.POST.getlist('budget_share')
        total_budget = sum(int(s) for s in shares if s)

        # 3. Create the Main Event record
        new_event = Events.objects.create(
            event_name=name,
            event_date=full_datetime,
            event_details=details,
            event_type=event_type,
            event_fee=fee,
            venue=venue,
            budget=total_budget
        )

        # 4. Create ClubsEvents record for the Host
        ClubsEvents.objects.create(
            club_id=hosting_club.club_id, # Storing the ID string
            event=new_event,
            role='Host',
            budget_share=int(shares[0]) if shares[0] else 0
        )

        # 5. Create ClubsEvents records for Partners
        partner_ids = request.POST.getlist('partner_club_ids')
        # Partners start from the second index in the 'shares' list
        for i, p_id in enumerate(partner_ids):
            ClubsEvents.objects.create(
                club_id=p_id,
                event=new_event,
                role='Partner',
                budget_share=int(shares[i+1]) if shares[i+1] else 0
            )

        return redirect('exec_dashboard', club_id=club_id)

    all_clubs = Clubs.objects.exclude(club_id=club_id)
    return render(request, 'dashboard/create_event.html', {
        'club': hosting_club,
        'all_clubs': all_clubs
    })

@login_required
def event_detail_view(request, event_id):
    event = get_object_or_404(Events, event_id=event_id)
    student = Students.objects.get(email=request.user.user_email)

    # Fetch involvements, hosting/partnered clubs
    club_involvements = ClubsEvents.objects.filter(event=event)
    hosting_clubs = []
    partnered_clubs = []
    
    for involvement in club_involvements:
        club_obj = Clubs.objects.filter(club_id=involvement.club_id).first()
        if club_obj:
            if involvement.role == 'Host':
                hosting_clubs.append(club_obj)
            else:
                partnered_clubs.append(club_obj)

    # Fetch registration and volunteer objects
    reg_object = EventRegistration.objects.filter(student=student, event=event).first()
    is_registered = reg_object is not None
    
    vol_object = Volunteers.objects.filter(student=student, event=event).first()
    is_volunteer = vol_object is not None

    # Logic for Review Permissions
    # Only allow review if they have a successful registration
    can_review = reg_object and reg_object.payment_status == 'Success'

    if request.method == "POST":
        action = request.POST.get('action')
        
        # Action: Registration
        if action == 'attend' and not is_registered:
            EventRegistration.objects.create(
                student=student,
                event=event,
                payment_status='Unpaid',
                attendance='Absent'
            )
            return redirect('event_detail', event_id=event_id)
            
        # Action: Volunteering
        elif action == 'volunteer' and not is_volunteer:
            Volunteers.objects.create(
                student=student,
                event=event,
                role='Pending'
            )
            return redirect('event_detail', event_id=event_id)

        # Action: Feedback (NEW)
        elif action == 'submit_feedback' and can_review:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            
            # Update the existing registration record
            reg_object.rating = rating
            reg_object.comment = comment
            reg_object.save()
            return redirect('event_detail', event_id=event_id)

    return render(request, 'dashboard/event_detail.html', {
        'event': event,
        'hosting_clubs': hosting_clubs,
        'partnered_clubs': partnered_clubs,
        'reg_object': reg_object,
        'is_registered': is_registered,
        'is_volunteer': is_volunteer,
        'vol_object': vol_object,
        'can_review': can_review, # Pass permission to template
    })

@login_required
def all_events_view(request):
    search_query = request.GET.get('search', '')
    
    # Base Queryset
    events = Events.objects.all().order_by('event_date')
    
    # Apply Search Filter
    if search_query:
        events = events.filter(
            Q(event_name__icontains=search_query) |
            Q(event_type__icontains=search_query) |
            Q(venue__icontains=search_query)
        )
    
    # Keep sidebar clubs populated
    student = Students.objects.get(email=request.user.user_email)
    my_clubs = ClubsMembers.objects.filter(student=student).select_related('club')

    return render(request, 'dashboard/all_events.html', {
        'all_events': events,
        'my_clubs': my_clubs
    })

@login_required
def approve_event_registration(request, registration_id):
    reg = get_object_or_404(EventRegistration, registration_id=registration_id)
    if request.method == "POST":
        reg.payment_status = 'Success'
        reg.save()
        messages.success(request, f"Approved {reg.student.name}")

    # Redirect back to the specific event management page
    return redirect('manage_specific_event', event_id=reg.event.event_id)

@login_required
def reject_event_reg(request, registration_id):
    reg = get_object_or_404(EventRegistration, registration_id=registration_id)
    event_id = reg.event.event_id
    if request.method == "POST":
        reg.delete()
        messages.warning(request, "Registration rejected.")

    # Redirect back to the specific event management page
    return redirect('manage_specific_event', event_id=event_id)

# views.py
@login_required
def club_events_list(request, club_id):
    club = get_object_or_404(Clubs, club_id=club_id)
    event_links = ClubsEvents.objects.filter(club_id=club_id).select_related('event')
    
    # Use timezone.now() for accurate DateTime comparison
    return render(request, 'dashboard/club_events_list.html', {
        'club': club,
        'event_links': event_links,
        'current_time': timezone.now() 
    })

@login_required
def manage_specific_event(request, event_id):
    event = get_object_or_404(Events, event_id=event_id)
    club_link = ClubsEvents.objects.filter(event=event).first()
    
    club = None
    if club_link:
        club = Clubs.objects.filter(club_id=club_link.club_id).first()
    
    pending_requests = EventRegistration.objects.filter(event=event, payment_status='Unpaid')
    confirmed_attendees = EventRegistration.objects.filter(event=event, payment_status='Success')
    
    # 1. Get current month and year
    now = timezone.now()
    
    # 2. Fetch pending volunteers
    pending_vols = Volunteers.objects.filter(event=event, role='Pending')
    
    # 3. Calculate monthly activity for each volunteer
    now = timezone.now()
    for vol in pending_vols:
        vol.monthly_count = Volunteers.objects.filter(
            student=vol.student,
            role='Approved',
            volunteer_date__month=now.month,
            volunteer_date__year=now.year
        ).count()

    approved_vols = Volunteers.objects.filter(event=event, role='Approved')

    return render(request, 'dashboard/manage_event.html', {
        'event': event,
        'club': club,
        'pending_requests': pending_requests,
        'confirmed_attendees': confirmed_attendees,
        'pending_vols': pending_vols, # Now contains .monthly_count
        'approved_vols': approved_vols
    })

@login_required
def approve_volunteer(request, vol_id):
    # Fetch the specific volunteer record
    volunteer = get_object_or_404(Volunteers, volunteer_id=vol_id)
    
    # Get budget from GET parameters
    budget = request.GET.get('budget', 0)
    try:
        budget_value = float(budget)
    except (ValueError, TypeError):
        budget_value = 0

    # Update the volunteer record
    volunteer.role = 'Approved'
    volunteer.budget_allocated = budget_value 
    
    # FIX: Set the date to the EVENT'S date, not the current timestamp
    # This ensures the monthly activity count is based on when the work happens
    volunteer.volunteer_date = volunteer.event.event_date 
    
    volunteer.save()
    
    # Redirect back to the management page
    return redirect('manage_specific_event', event_id=volunteer.event.event_id)

@login_required
def reject_volunteer(request, vol_id):
    # Fetch the record using volunteer_id to avoid FieldError
    vol = get_object_or_404(Volunteers, volunteer_id=vol_id)
    event_id = vol.event.event_id
    
    # This will now run for both GET and POST requests
    vol.delete()
        
    return redirect('manage_specific_event', event_id=event_id)