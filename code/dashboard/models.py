# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Alert(models.Model):
    alert_id = models.CharField(db_column='Alert_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    club = models.ForeignKey('Clubs', models.CASCADE, db_column='Club_ID', blank=True, null=True)  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=255, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_at', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'alert'


class Assets(models.Model):
    asset_id = models.CharField(db_column='Asset_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    club = models.ForeignKey('Clubs', models.CASCADE, db_column='Club_ID', blank=True, null=True)  # Field name made lowercase.
    asset_name = models.CharField(db_column='Asset_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'assets'


class Clubs(models.Model):
    club_id = models.CharField(db_column='Club_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    club_name = models.CharField(db_column='Club_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    club_funds = models.IntegerField(db_column='Club_Funds', blank=True, null=True)  # Field name made lowercase.
    reg_fee = models.IntegerField(db_column='Reg_fee', blank=True, null=True)  # Field name made lowercase.
    advisor_name = models.CharField(db_column='Advisor_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    advisor_email = models.CharField(db_column='Advisor_Email', max_length=50, blank=True, null=True)  # Field name made lowercase.
    advisor_initial = models.CharField(db_column='Advisor_Initial', max_length=50, blank=True, null=True)  # Field name made lowercase.
    founded_year = models.TextField(db_column='Founded_Year', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'clubs'


class ClubsEvents(models.Model):
    club_id = models.CharField(db_column='Club_ID', max_length=10, primary_key=True)  # Field name made lowercase.
    event = models.ForeignKey('Events', models.CASCADE, db_column='Event_ID')  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=50, blank=True, null=True)  # Field name made lowercase.
    budget_share = models.IntegerField(db_column='Budget_share', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        unique_together = (('club_id', 'event'),)
        db_table = 'clubs_events'


class ClubsMembers(models.Model):
    club = models.ForeignKey('Clubs', on_delete=models.CASCADE, db_column='Club_ID', primary_key=True)
    student = models.ForeignKey('Students', on_delete=models.CASCADE, db_column='Student_ID', unique=True)
    role = models.ForeignKey('Roles', models.CASCADE, db_column='Role_ID', blank=True, null=True)  # Field name made lowercase.
    joining_date = models.DateTimeField(db_column='Joining_date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        unique_together = (('club', 'student'),)
        db_table = 'clubs_members'


class ClubsRegistration(models.Model):
    club = models.ForeignKey(Clubs, models.CASCADE, db_column='Club_ID', primary_key=True)  # Field name made lowercase.
    student = models.ForeignKey('Students', models.CASCADE, db_column='Student_ID')  # Field name made lowercase.
    payment_status = models.CharField(db_column='Payment_status', max_length=7, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        unique_together = (('club', 'student'),)
        db_table = 'clubs_registration'


class EventRegistration(models.Model):
    registration_id = models.CharField(db_column='Registration_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    student = models.ForeignKey('Students', models.CASCADE, db_column='Student_ID', blank=True, null=True)  # Field name made lowercase.
    event = models.ForeignKey('Events', models.CASCADE, db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    attendance_code = models.TextField(db_column='Attendance_code', blank=True, null=True)  # Field name made lowercase.
    attendance = models.CharField(db_column='Attendance', max_length=7, blank=True, null=True)  # Field name made lowercase.
    attendance_time = models.DateTimeField(db_column='Attendance_time', blank=True, null=True)  # Field name made lowercase.
    rating = models.PositiveIntegerField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=255, blank=True, null=True)  # Field name made lowercase.
    payment_status = models.CharField(db_column='Payment_status', max_length=7, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'event_registration'


class Events(models.Model):
    event_id = models.CharField(db_column='Event_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    event_name = models.CharField(db_column='Event_Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    event_date = models.DateTimeField(db_column='Event_Date', blank=True, null=True)  # Field name made lowercase.
    event_details = models.CharField(db_column='Event_details', max_length=255, blank=True, null=True)  # Field name made lowercase.
    event_type = models.CharField(db_column='Event_type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    event_fee = models.IntegerField(db_column='Event_fee', blank=True, null=True)  # Field name made lowercase.
    venue = models.CharField(db_column='Venue', max_length=50, blank=True, null=True)  # Field name made lowercase.
    budget = models.IntegerField(db_column='Budget', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'events'


class Expenses(models.Model):
    expenses_id = models.CharField(db_column='Expenses_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    volunteer = models.ForeignKey('Volunteers', models.SET_NULL, db_column='Volunteer_ID', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'expenses'


class Loans(models.Model):
    loan_id = models.CharField(db_column='Loan_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    asset = models.ForeignKey(Assets, models.CASCADE, db_column='Asset_ID', blank=True, null=True)  # Field name made lowercase.
    lender_club = models.ForeignKey(ClubsMembers, models.SET_NULL, db_column='Lender_Club_ID', blank=True, null=True)  # Field name made lowercase.
    lender_student = models.ForeignKey(ClubsMembers, models.SET_NULL, db_column='Lender_Student_ID', to_field='student', related_name='loans_lender_student_set', blank=True, null=True)  # Field name made lowercase.
    borrower_club = models.ForeignKey(ClubsMembers, models.SET_NULL, db_column='Borrower_Club_ID', related_name='loans_borrower_club_set', blank=True, null=True)  # Field name made lowercase.
    borrower_student = models.ForeignKey(ClubsMembers, models.SET_NULL, db_column='Borrower_Student_ID', to_field='student', related_name='loans_borrower_student_set', blank=True, null=True)  # Field name made lowercase.
    borrow_date = models.DateTimeField(db_column='Borrow_date', blank=True, null=True)  # Field name made lowercase.
    return_date = models.DateTimeField(db_column='return_date',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loans'


class Roles(models.Model):
    role_id = models.CharField(db_column='Role_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'roles'


class Skills(models.Model):
    student = models.ForeignKey('Students', on_delete=models.CASCADE, db_column='Student_ID', primary_key=True)
    skill = models.CharField(db_column='Skill', max_length=50)

    class Meta:
        managed = False
        unique_together = (('student', 'skill'),)
        db_table = 'skills'


class Students(models.Model):
    student_id = models.CharField(db_column='Student_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.ForeignKey('Users', models.CASCADE, db_column='Email', blank=True, null=True)  # Field name made lowercase.
    department = models.CharField(db_column='Department', max_length=50, blank=True, null=True)  # Field name made lowercase.
    personality_type = models.CharField(db_column='Personality_type', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'students'


class UserManager(BaseUserManager):
    def create_user(self, user_email, password=None):
        if not user_email:
            raise ValueError('Users must have an email address')
        user = self.model(user_email=self.normalize_email(user_email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_email, password=None):
        user = self.create_user(user_email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    user_email = models.EmailField(db_column='User_Email', primary_key=True, max_length=50)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(db_column='last_login', blank=True, null=True)  # Field name made lowercase.
    account_created = models.DateTimeField(db_column='Account_Created',auto_now_add=True, blank=True, null=True)  # Field name made lowercase.
    objects = UserManager()
    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = []


    class Meta:
        managed = False
        db_table = 'users'


class Volunteers(models.Model):
    volunteer_id = models.CharField(db_column='Volunteer_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    event = models.ForeignKey(Events, models.CASCADE, db_column='Event_ID', blank=True, null=True)  # Field name made lowercase.
    student = models.ForeignKey(Students, models.CASCADE, db_column='Student_ID', blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=255, blank=True, null=True)  # Field name made lowercase.
    budget_allocated = models.IntegerField(db_column='Budget_allocated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'volunteers'
