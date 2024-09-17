from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'address', 'gender', 'specialization', 'password1', 'password2', 'role'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if obj is None:  # Adding a new user
            return [
                (None, {'fields': ('username', 'password1', 'password2')}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'gender', 'role', 'specialization')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
            ]
        else:  # Editing an existing user
            return [
                (None, {'fields': ('username', 'password')}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'gender', 'role', 'specialization')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
            ]
            

    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role', 'specialization')

    def get_list_display(self, request):
        # Customize list display based on user role or admin preferences
        return ('username', 'first_name', 'last_name', 'email', 'role')

admin.site.register(User, UserAdmin)
