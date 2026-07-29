from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Add custom fields to the edit form in admin
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('telegram_id', 'phone_number', 'role', 'language', 'loyalty_coins', 'date_of_birth')}),
    )
    
    # Add custom fields to the user list table in admin
    list_display = BaseUserAdmin.list_display + ('role', 'telegram_id', 'loyalty_coins', 'date_of_birth')

admin.site.register(User, UserAdmin)