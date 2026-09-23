from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser

CustomUser._meta.app_label = 'auth'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass
