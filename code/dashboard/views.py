from urllib import request
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.db.models import Q,Count
from .models import Alert, Clubs, ClubsEvents, Loans, Users, Students,Clubs, ClubsMembers, Events,EventRegistration, ClubsRegistration, Volunteers, Expenses, Skills, Assets
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.mail import EmailMessage
from datetime import datetime

from dashboard import models

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'dashboard/login.html')
            
    return render(request, 'dashboard/login.html')

def register_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        
        if Students.objects.filter(student_id=student_id).exists():
            messages.error(request, f"Student ID {student_id} is already registered.")
            return render(request, 'dashboard/login.html', {'show_register_modal': True})

        if Students.objects.filter(email=email).exists():
            messages.error(request, "This email is already associated with an account.")
            return render(request, 'dashboard/login.html', {'show_register_modal': True})
        
    if request.method == "POST":
        # Get data from form
        sid = request.POST.get('student_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        pw = request.POST.get('password')
        dept = request.POST.get('department')
        ptype = request.POST.get('personality')

        try:
            with transaction.atomic():
                new_user = Users(user_email=email)
                new_user.set_password(pw)
                new_user.save()

                new_student = Students(
                    student_id=sid,
                    name=name,
                    email=new_user,
                    department=dept,
                    personality_type=ptype
                )
                new_student.save()

            return redirect('login')
        except Exception as e:
            return render(request, 'dashboard/login.html', {'error': f'Registration failed: {e}'})
        
@login_required
def home_view(request):

    upcoming_focus_events = Events.objects.all().order_by('event_date')[:3]
    
    try:
        current_student = Students.objects.get(email=request.user.user_email)
        my_clubs = ClubsMembers.objects.filter(student=current_student).select_related('club')
        registrations = EventRegistration.objects.filter(student=current_student).select_related('event')
        
    except Students.DoesNotExist:
        my_clubs = []
        registrations = []

    context = {
        'events': upcoming_focus_events,
        'my_registrations': registrations,
        'my_clubs': my_clubs,
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def all_clubs_view(request):
    clubs = Clubs.objects.all()
    
    try:
        student = Students.objects.get(email=request.user.user_email)
        my_clubs = ClubsMembers.objects.filter(student=student).select_related('club')
        
        joined_club_ids = list(my_clubs.values_list('club_id', flat=True))
        pending_club_ids = list(ClubsRegistration.objects.filter(student=student).values_list('club_id', flat=True))
        
    except Students.DoesNotExist:
        my_clubs = []
        joined_club_ids = []
        pending_club_ids = []

    return render(request, 'dashboard/all_clubs.html', {
        'clubs': clubs,
        'my_clubs': my_clubs,
        'joined_club_ids': joined_club_ids,
        'pending_club_ids': pending_club_ids,
    })

@login_required
def join_club_request(request, club_id):
    try:
        student = Students.objects.get(email=request.user.user_email)
        club = Clubs.objects.get(club_id=club_id)
        

        if ClubsMembers.objects.filter(student=student, club=club).exists():
            messages.info(request, "You are already a member of this club.")
            return redirect('all_clubs')

        if ClubsRegistration.objects.filter(student=student, club=club).exists():
            messages.warning(request, "Your membership request is already pending.")
            return redirect('all_clubs')

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
    club = get_object_or_404(Clubs, club_id=club_id)
    membership = get_object_or_404(ClubsMembers, student=student, club=club)
    event_links = ClubsEvents.objects.filter(club_id=club.club_id).select_related('event')
    club_events = [link.event for link in event_links]
    club_event_ids = [link.event.event_id for link in event_links]
    all_members = ClubsMembers.objects.filter(club=club).select_related('student')
    my_clubs = ClubsMembers.objects.filter(student=student).select_related('club')

    if request.method == "POST" and request.POST.get('action') == 'create_alert':
        message = request.POST.get('message')
        if membership.role in ['President', 'Vice President', 'Executive'] and message:
            Alert.objects.create(
                club=club,
                message=message,
                created_at=timezone.now()
            )
            messages.success(request, "Alert broadcasted successfully!")
            return redirect('club_dashboard', club_id=club_id)

    alerts = Alert.objects.filter(club=club).order_by('-created_at')

    context = {
        'club': club,
        'my_clubs': my_clubs,
        'all_members': all_members,
        'club_events': club_events, 
        'role': membership.role,
        'alerts': alerts, 
    }

    if membership.role in ['President', 'Vice President', 'Executive']:
        context['pending_requests'] = ClubsRegistration.objects.filter(club=club)
        context['event_reg_requests'] = EventRegistration.objects.filter(
            event_id__in=club_event_ids, 
            payment_status='Unpaid'
        ).select_related('student', 'event')
        return render(request, 'dashboard/exec_dashboard.html', context)
    else:
        return render(request, 'dashboard/members_view.html', context)
    
@login_required
def approve_event_registration(request, reg_id):
    registration = get_object_or_404(EventRegistration, registration_id=reg_id)
    
    if request.method == "POST":
        registration.payment_status = "Success"
        registration.attendance = "Absent"

        scan_url = request.build_absolute_uri(f"/events/scan/{registration.registration_id}/")
        

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(scan_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_image_data = buffer.getvalue()
        
        registration.save()

        subject = f"Registration Confirmed: {registration.event.event_name}"
        message = (
            f"Hi {registration.student.name},\n\n"
            f"Your registration for {registration.event.event_name} is confirmed!\n"
            f"Time: {registration.event.start_time}\n\n"
            "Please present the attached QR code at the entrance for attendance."
        )
        
        email = EmailMessage(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [registration.student.email.user_email]
        )
        email.attach(f'attendance_qr_{reg_id}.png', qr_image_data, 'image/png')
        email.send()

        messages.success(request, "Registration approved and QR code sent.")
        
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def scan_attendance(request, reg_id):  
    registration = get_object_or_404(EventRegistration, registration_id=reg_id)
    
    if registration.attendance == "Present":
        messages.info(request, f"{registration.student.name} is already marked present.")
    else:
        registration.attendance = "Present"
        registration.attendance_time = timezone.now()
        registration.save()
        messages.success(request, f"Attendance recorded for {registration.student.name} at {registration.attendance_time}")
    
    return render(request, 'dashboard/scan_result.html', {'registration': registration})
    
@login_required
def approve_member(request, reg_id):
    if request.method == 'POST':
        pending = get_object_or_404(ClubsRegistration, reg_id=reg_id)
        club_id = pending.club.club_id
        
        with transaction.atomic():
            ClubsMembers.objects.create(
                student=pending.student,
                club=pending.club,
                role='General Member'
            )
            pending.delete()
            
        messages.success(request, f"Approved {pending.student.email} successfully!")
        return redirect('club_dashboard', club_id=club_id)
    
@login_required
def reject_member(request, reg_id):
    if request.method == 'POST':
        pending = get_object_or_404(ClubsRegistration, reg_id=reg_id)
        club_id = pending.club.club_id
        pending.delete()
        
        messages.warning(request, "Membership request rejected.")
        return redirect('club_dashboard', club_id=club_id)

@login_required
def toggle_registration(request, club_id):
    if request.method == "POST":
        club = get_object_or_404(Clubs, club_id=club_id)
        
        is_exec = ClubsMembers.objects.filter(
            student__email=request.user.user_email, 
            club=club, 
            role__in=['President', 'Vice President', 'Secretary', 'Treasurer']
        ).exists()

        if is_exec:
            club.reg_open = not club.reg_open 
            club.save()
            status = "Open" if club.reg_open else "Closed"
            messages.success(request, f"Registration is now {status} for {club.club_name}.")
        else:
            messages.error(request, "You do not have permission to change this setting.")
            
    return redirect('club_dashboard', club_id=club_id)

def create_event_page(request, club_id):
    hosting_club = get_object_or_404(Clubs, club_id=club_id)
    
    if request.method == "POST":
        name = request.POST.get('event_name')
        date_str = request.POST.get('event_date')
        time_str = request.POST.get('event_time')
        venue = request.POST.get('venue')
        details = request.POST.get('details')
        event_type = request.POST.get('event_type')
        fee = request.POST.get('event_fee') or 0
        
        full_datetime = None
        if date_str and time_str:
            full_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

        shares = request.POST.getlist('budget_share')
        total_budget = sum(int(s) for s in shares if s)

        new_event = Events.objects.create(
            event_name=name,
            event_date=full_datetime,
            event_details=details,
            event_type=event_type,
            event_fee=fee,
            venue=venue,
            budget=total_budget
        )

        ClubsEvents.objects.create(
            club_id=hosting_club.club_id,
            event=new_event,
            role='Host',
            budget_share=int(shares[0]) if shares[0] else 0
        )

        partner_ids = request.POST.getlist('partner_club_ids')
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

    reg_object = EventRegistration.objects.filter(student=student, event=event).first()
    is_registered = reg_object is not None
    
    vol_object = Volunteers.objects.filter(student=student, event=event).first()
    is_volunteer = vol_object is not None

    can_review = reg_object and reg_object.payment_status == 'Success'
    is_approved_volunteer = vol_object and vol_object.role == 'Approved'
    
    volunteer_expenses = []
    total_spent = 0
    remaining_budget = 0
    if is_approved_volunteer:
        volunteer_expenses = Expenses.objects.filter(volunteer=vol_object)
        total_spent = sum(exp.amount for exp in volunteer_expenses if exp.amount)
        budget_allocated = vol_object.budget_allocated or 0
        remaining_budget = budget_allocated - total_spent

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'attend':
            if is_volunteer:
                messages.error(request, "You are already a volunteer and cannot register as an attendee.")
            elif not is_registered:
                EventRegistration.objects.create(
                    student=student, event=event,
                    payment_status='Unpaid', attendance='Absent'
                )
                return redirect('event_detail', event_id=event_id)

        elif action == 'volunteer':
            if is_registered:
                messages.error(request, "You are already an attendee and cannot apply to volunteer.")
            elif not is_volunteer:
                Volunteers.objects.create(
                    student=student, event=event, role='Pending'
                )
                return redirect('event_detail', event_id=event_id)

        elif action == 'submit_feedback' and can_review:
            reg_object.rating = request.POST.get('rating')
            reg_object.comment = request.POST.get('comment')
            reg_object.save()
            return redirect('event_detail', event_id=event_id)

        elif action == 'submit_expense' and is_approved_volunteer:
            description = request.POST.get('description', '').strip()
            amount_str = request.POST.get('amount', '').strip()

            if not description or not amount_str:
                messages.error(request, "Both description and amount are required.")
            else:
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        messages.error(request, "Amount must be greater than zero.")
                    elif vol_object.budget_allocated and (total_spent + amount > vol_object.budget_allocated):
                        messages.warning(request, "This expense exceeds your allocated budget!")
                    else:
                        Expenses.objects.create(
                            volunteer=vol_object,
                            description=description,
                            amount=amount
                        )
                except ValueError:
                    messages.error(request, "Please enter a valid number for the amount.")
            
            return redirect('event_detail', event_id=event_id)

    return render(request, 'dashboard/event_detail.html', {
        'event': event,
        'hosting_clubs': hosting_clubs,
        'partnered_clubs': partnered_clubs,
        'reg_object': reg_object,
        'is_registered': is_registered,
        'is_volunteer': is_volunteer,
        'vol_object': vol_object,
        'can_review': can_review,
        'is_approved_volunteer': is_approved_volunteer,
        'volunteer_expenses': volunteer_expenses,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
    })

@login_required
def all_events_view(request):
    search_query = request.GET.get('search', '')
    events = Events.objects.all().order_by('event_date')
    
    if search_query:
        events = events.filter(
            Q(event_name__icontains=search_query) |
            Q(event_type__icontains=search_query) |
            Q(venue__icontains=search_query)
        )
    
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

    return redirect('manage_specific_event', event_id=reg.event.event_id)

@login_required
def reject_event_reg(request, registration_id):
    reg = get_object_or_404(EventRegistration, registration_id=registration_id)
    event_id = reg.event.event_id
    if request.method == "POST":
        reg.delete()
        messages.warning(request, "Registration rejected.")

    return redirect('manage_specific_event', event_id=event_id)

@login_required
def club_events_list(request, club_id):
    club = get_object_or_404(Clubs, club_id=club_id)
    event_links = ClubsEvents.objects.filter(club_id=club_id).select_related('event')
    
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
    
    now = timezone.now()
    
    pending_vols = Volunteers.objects.filter(event=event, role='Pending')
    
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
        'pending_vols': pending_vols,
        'approved_vols': approved_vols
    })

@login_required
def approve_volunteer(request, vol_id):
    volunteer = get_object_or_404(Volunteers, volunteer_id=vol_id)
    
    budget = request.GET.get('budget', 0)
    try:
        budget_value = float(budget)
    except (ValueError, TypeError):
        budget_value = 0

    volunteer.role = 'Approved'
    volunteer.budget_allocated = budget_value 
    volunteer.volunteer_date = volunteer.event.event_date 
    volunteer.save()
    
    return redirect('manage_specific_event', event_id=volunteer.event.event_id)

@login_required
def reject_volunteer(request, vol_id):
    vol = get_object_or_404(Volunteers, volunteer_id=vol_id)
    event_id = vol.event.event_id
    vol.delete()
        
    return redirect('manage_specific_event', event_id=event_id)

@login_required
def create_alert(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        club_id = request.POST.get('club_id')
        
        if subject and message and club_id:
            club = get_object_or_404(Clubs, club_id=club_id)
            Alert.objects.create(
                club=club,
                subject=subject,
                message=message,
                created_at=timezone.now()
            )
            messages.success(request, "Alert broadcasted successfully!")
        else:
            messages.error(request, "Both Subject and Message are required.")
            
    return redirect(request.META.get('HTTP_REFERER', 'club_dashboard'))

@login_required
def delete_alert(request, alert_id):
    alert = get_object_or_404(Alert, alert_id=alert_id)
    
    membership = ClubsMembers.objects.filter(
        student__email=request.user.user_email, 
        club=alert.club
    ).first()

    if membership and membership.role in ['President', 'Vice President', 'Executive']:
        alert.delete()
        messages.success(request, "Alert deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this alert.")

    return redirect(request.META.get('HTTP_REFERER', 'club_dashboard'))

@login_required
def profile_view(request):
    student = get_object_or_404(Students, email=request.user.user_email)
    skills = Skills.objects.filter(student=student)
    
    participated_events = EventRegistration.objects.filter(
        student=student, 
        attendance='Present' 
    ).select_related('event')
    
    volunteered_events = Volunteers.objects.filter(
        student=student, 
        role='Approved'
    ).select_related('event')

    return render(request, 'dashboard/profile.html', {
        'student': student,
        'skills': skills,
        'events_attended_count': participated_events.count(),
        'events_volunteered_count': volunteered_events.count(),
        'participated_events': participated_events,
        'volunteered_events': volunteered_events,
    })

@login_required
def add_skill(request):
    if request.method == 'POST':
        student = get_object_or_404(Students, email=request.user.user_email)
        skill_name = request.POST.get('skill_name').strip()
        
        if skill_name:
            Skills.objects.create(student=student, skill=skill_name)
            messages.success(request, f"Skill '{skill_name}' added!")
            
    return redirect('profile')

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skills, skill_id=skill_id)
    if skill.student.email == request.user.user_email:
        skill.delete()
    return redirect('profile')

@login_required
def asset_management(request, club_id):
    current_view_club = get_object_or_404(Clubs, club_id=club_id)
    user_member_ids = ClubsMembers.objects.filter(
        student__email__user_email=request.user.user_email
    ).values_list('member_id', flat=True)

    already_requested_ids = list(Loans.objects.filter(
        borrower_member_id__in=user_member_ids, 
        status='Pending'
    ).values_list('asset_id', flat=True))

    unavailable_asset_ids = Loans.objects.filter(
        status__in=['Approved']
    ).values_list('asset_id', flat=True)

    my_assets = Assets.objects.filter(club=current_view_club)
    other_assets = Assets.objects.exclude(club=current_view_club).exclude(asset_id__in=unavailable_asset_ids)

    lend_requests = Loans.objects.filter(asset__club=current_view_club, status='Pending')
    currently_lended = Loans.objects.filter(
        asset__club=current_view_club, 
        status='Approved', 
        return_date__isnull=True
    ).exclude(borrower_member__club=current_view_club)

    currently_borrowed = Loans.objects.filter(
        borrower_member__club=current_view_club, 
        status='Approved', 
        return_date__isnull=True
    ).exclude(asset__club=current_view_club)

    return render(request, 'dashboard/asset_management.html', {
        'club': current_view_club,
        'my_assets': my_assets,
        'other_assets': other_assets,
        'already_requested_ids': already_requested_ids,
        'lend_requests': lend_requests,
        'currently_lended': currently_lended,
        'currently_borrowed': currently_borrowed
    })

@login_required
def request_borrow(request, asset_id, club_id):
    asset = get_object_or_404(Assets, asset_id=asset_id)
    
    is_already_lent = Loans.objects.filter(asset=asset, status='Approved').exists()

    if is_already_lent:
        messages.error(request, f"Sorry, {asset.asset_name} is currently unavailable.")
        return redirect('asset_management', club_id=club_id)

    borrower_member = ClubsMembers.objects.get(
        student__email__user_email=request.user.user_email, 
        club_id=club_id
    )
    
    Loans.objects.create(
        asset=asset,
        borrower_member=borrower_member,
        status='Pending'
    )
    return redirect('asset_management', club_id=club_id)

@login_required
def approve_loan(request, loan_id):
    if request.method == "POST":
        loan = get_object_or_404(Loans, loan_id=loan_id)
        approver = ClubsMembers.objects.filter(
            student__email__user_email=request.user.user_email, 
            club=loan.asset.club
        ).first()
        
        if approver:
            already_lent = Loans.objects.filter(asset=loan.asset, status='Approved').exists()
            if already_lent:
                messages.error(request, "This item is already lent to another club.")
                return redirect(request.META.get('HTTP_REFERER'))

            loan.status = 'Approved'
            loan.lender_member = approver 
            loan.save()
            messages.success(request, f"Loan for {loan.asset.asset_name} approved.")
        else:
            messages.error(request, "Permission denied.")
            
    return redirect(request.META.get('HTTP_REFERER', 'asset_management'))

@login_required
def reject_loan(request, loan_id):
    if request.method == "POST":
        loan = get_object_or_404(Loans, loan_id=loan_id)
        
        rejector = ClubsMembers.objects.filter(
            student__email__user_email=request.user.user_email, 
            club=loan.asset.club
        ).first()
        
        if rejector:
            loan.status = 'Rejected'
            loan.lender_member = rejector  
            loan.save()
            messages.info(request, "Loan request rejected.")
            
    return redirect(request.META.get('HTTP_REFERER', 'asset_management'))

@login_required
def return_asset(request, loan_id):
    if request.method == "POST":
        loan = get_object_or_404(Loans, loan_id=loan_id)
        loan.return_date = timezone.now()
        loan.status = 'Returned'
        loan.save()
        messages.success(request, f"Item {loan.asset.asset_name} marked as returned.")
    return redirect(request.META.get('HTTP_REFERER', 'asset_management'))

@login_required
def add_asset(request, club_id):
    if request.method == 'POST':
        club = get_object_or_404(Clubs, club_id=club_id)
        asset_name = request.POST.get('asset_name')
        category = request.POST.get('category')
        
        Assets.objects.create(
            club=club,
            asset_name=asset_name,
            category=category
        )
        messages.success(request, "Asset added to inventory.")
    
    return redirect('asset_management', club_id=club_id)