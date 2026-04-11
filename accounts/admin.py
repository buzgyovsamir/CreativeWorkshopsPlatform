from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {
            'fields': ('profile_image', 'bio', 'city'),
        }),
    )