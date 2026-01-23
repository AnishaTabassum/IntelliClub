from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # --- Authentication & General ---
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('events/', views.all_events_view, name='all_events'),
    path('event/<int:event_id>/', views.event_detail_view, name='event_detail'),

    # --- Club Management ---
    path('clubs/', views.all_clubs_view, name='all_clubs'),
    path('club/join/<int:club_id>/', views.join_club_request, name='join_club'),
    path('club/dashboard/<int:club_id>/', views.club_dashboard_view, name='club_dashboard'),
    path('club/toggle-reg/<int:club_id>/', views.toggle_registration, name='toggle_registration'),
    
    # --- Executive Actions (Member Requests) ---
    path('club/approve/<int:reg_id>/', views.approve_member, name='approve_member'),
    path('club/reject/<int:reg_id>/', views.reject_member, name='reject_member'),

    # --- NEW: Organized Event Management Flow ---
    # 1. Page to see all event cards for a club
    path('club/<int:club_id>/events/', views.club_events_list, name='club_events_list'),
    
    # 2. Page to manage a specific event (Details + Requests + Attendees)
    path('event/manage/<int:event_id>/', views.manage_specific_event, name='manage_specific_event'),
    
    # 3. Create Event
    path('club/<int:club_id>/create-event/', views.create_event_page, name='create_event_page'),

    # --- Event Registration Actions (Ajax/Post) ---
    path('approve-event-reg/<int:registration_id>/', views.approve_event_registration, name='approve_event_reg'),
    path('reject-event/<int:registration_id>/', views.reject_event_reg, name='reject_event_reg'),

    path('approve-volunteer/<int:vol_id>/', views.approve_volunteer, name='approve_volunteer'),
    path('reject-volunteer/<int:vol_id>/', views.reject_volunteer, name='reject_volunteer'),

    path('create-alert/', views.create_alert, name='create_alert'),
    path('delete-alert/<int:alert_id>/', views.delete_alert, name='delete_alert'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/add-skill/', views.add_skill, name='add_skill'),
    path('profile/delete-skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),

    path('club/<int:club_id>/assets/', views.asset_management, name='asset_management'),
    path('assets/borrow/<int:asset_id>/', views.request_borrow, name='request_borrow'),
    path('assets/approve/<int:loan_id>/', views.approve_loan, name='approve_loan'),
    path('assets/return/<int:loan_id>/', views.return_asset, name='return_asset'),
    path('loans/reject/<int:loan_id>/', views.reject_loan, name='reject_loan'),
    path('club/<int:club_id>/assets/add/', views.add_asset, name='add_asset'),
    path('loans/return/<int:loan_id>/', views.return_asset, name='return_asset'),
]