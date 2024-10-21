from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email: 
            raise ValueError("You have not provided a valid email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    # def create_finance_admin(self, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_financeadmin', True)
    #     return self._create_user(email, password, **extra_fields)
    
    # def create_shopowner(self, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_active', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(email, password, **extra_fields)
    
    # def create_financeadmin(self, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     extra_fields.setdefault('is_financeadmin', True)
    #     return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    


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


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.first_name 

    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]
    
class Customer(models.Model):
    user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE, related_name='customer_profile', default='', unique=True)
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

class finance_team(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        primary_key=True,
        related_name='finance_team',
    )

    class Meta:
        verbose_name = 'finance_team'
        verbose_name_plural = 'finance_teams'                                 
        
