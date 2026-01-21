from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('clubs/', views.all_clubs_view, name='all_clubs'),
    path('club/join/<int:club_id>/', views.join_club_request, name='join_club'),
    path('club/dashboard/<int:club_id>/', views.club_dashboard_view, name='club_dashboard'),
    path('club/approve/<int:reg_id>/', views.approve_member, name='approve_member'),
]