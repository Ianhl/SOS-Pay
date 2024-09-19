from django.contrib import admin

# from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User, shop_owner, Customer, finance_team

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')

@admin.register(shop_owner)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name')

@admin.register(Customer)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'grad_year', 'year_group', 'hostel_group',)

@admin.register(finance_team)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)