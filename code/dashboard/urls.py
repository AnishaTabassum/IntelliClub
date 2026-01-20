from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('clubs/', views.all_clubs_view, name='all_clubs'),
]