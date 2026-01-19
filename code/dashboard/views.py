from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import transaction
from .models import Users, Students

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