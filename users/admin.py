from django.contrib import admin
from .models import User, UserConfirmation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'role', 'auth_status', 'is_verified', 'first_name', 'id']
    search_fields = ['phone', 'id']



@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'expiration_time', 'is_confirmed']
    search_fields = ['code', ]
