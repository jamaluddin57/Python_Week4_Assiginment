from django.contrib import admin
from .models import Appointment
from api.users.models import User

class AppointmentAdmin(admin.ModelAdmin):
    search_fields = ['doctor__first_name','doctor__last_name','patient__first_name' ,'patient__last_name', 'scheduled_at']
    list_filter = ['scheduled_at', 'created_at']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            kwargs["queryset"] = User.objects.filter(role=User.DOCTOR)
        else:
            kwargs["queryset"] = User.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Appointment, AppointmentAdmin)
