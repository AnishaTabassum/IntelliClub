from .models import Students, ClubsMembers

def sidebar_clubs(request):
    # This function makes 'my_clubs' available to EVERY page automatically
    if request.user.is_authenticated:
        try:
            # Match the student based on your custom user email logic
            student = Students.objects.get(email=request.user.user_email)
            # Fetch all clubs this specific student belongs to
            my_clubs = ClubsMembers.objects.filter(student=student).select_related('club')
            return {'my_clubs': my_clubs}
        except (Students.DoesNotExist, AttributeError):
            return {'my_clubs': []}
    return {'my_clubs': []}