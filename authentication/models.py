import random
import string
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

# Create your models here.

class CustomUserManager(UserManager):
    # Basic user creation function
    def _create_user(self, email, password, **extra_fields):
        if not email: 
            raise ValueError("You have not provided a valid email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    # Creates a basic user and sets admin and superuser status to false
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
     # Creates a superuser and sets admin and superuser status to True
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    

# This is the custom user model that allows login and authentication with email and password
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_financeadmin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

# The .objects points to the CustomUserManager which contains the methods for user creation
    objects = CustomUserManager() 
# The username field from the default user is replaced with the email to allow for authentication via email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.first_name 

    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]
    
# Create a customer instance linked to a specific user instance
class Customer(models.Model):
    # One to one field with an existing user instance
    user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE, related_name='customer_profile', default='', unique=True)
    # Choices for dropdown in the various selections. Passed to html template view
    year_choices = [
        ("MYP4", "MYP4"),
        ("MYP5", "MYP5"),
        ("DP1", "DP1"),
        ("DP2", "DP2"),
    ]
    hostel_group_choices = [
        ("Titan", "Titan"),
        ("Trojan", "Trojan"),
        ("Viking", "Viking"),
        ("Spartan", "Spartan"),
    ]
    hostel_choices = [
        ("Tana", "Tana"),
        ("Kariba", "Kariba"),
        ("Juba", "Juba"),
        ("Congo", "Congo"),
        ("Niger", "Niger"),
        ("Densu", "Densu"),
        ("Turkana", "Turkana"),
        ("Cavally", "Cavally"),
        ("Ankobra", "Ankobra"),
        ("Volta", "Volta"),
        ("Nile", "Nile"),
        ("Limpopo", "Limpopo"),
        ("Mano", "Mano"),
        ("Sassandra", "Sassandra"),
        ("Zambezi", "Zambezi"),
        ("Kagera", "Kagera"),
        ("Tanganyika", "Tanganyika"),
    ]
    grad_year = models.PositiveSmallIntegerField(blank=True, default=2025, null=True)
    year_group = models.CharField(max_length=255, default='', choices=year_choices)
    hostel_group = models.CharField(max_length=255, default='Titan', choices=hostel_group_choices)
    hostel = models.CharField(max_length=255, default='Tana', choices=hostel_choices)
    room_num = models.PositiveSmallIntegerField(blank=True, default=1, null=True)
    parent1_email = models.EmailField(blank=True, default='')
    parent1_first_name = models.CharField(max_length=255, blank=True, default='')
    parent1_last_name = models.CharField(max_length=255, blank=True, default='')
    parent2_email = models.EmailField(blank=True, default='')
    parent2_first_name = models.CharField(max_length=255, blank=True, default='')
    parent2_last_name = models.CharField(max_length=255, blank=True, default='')
    student_code = models.CharField(max_length=7, blank=True, default='', unique='True')

    # Customer model method that allows to create generate a student_code
    # Student code consists of the first three letters of the student last name and a unique 4 digit code
    def generate_student_code(self):
        length = 4
        characters =  string.digits
        while True:
            code = ''.join(random.choice(characters) for _ in range(length))
            lname= self.user.last_name
            lname = lname.upper()
            lname = lname[0:3]
            code = f'{lname}{code}'
            if not Customer.objects.filter(student_code=code).exists():
                return code    

    def __str__(self):
        return self.user.first_name

    

 
    
    
class shop_owner(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        primary_key=True,
        related_name='shop_owner',
    )
    vendor_name = models.CharField(max_length=256, null=True, blank=True)
    # shop = models.OneToOneField()  
    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
class tuckshop(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        primary_key=True,
        related_name='tuckshop_owner',
    )
    owner_name = models.CharField(max_length=256, null=True, blank=True)
    # shop = models.OneToOneField()  
    class Meta:
        verbose_name = 'Tuckshop'
        verbose_name_plural = 'Tuckshop'

class finance_team(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        primary_key=True,
        related_name='finance_team',
    )

    class Meta:
        verbose_name = 'finance_team'
        verbose_name_plural = 'finance_teams'                                 
        
