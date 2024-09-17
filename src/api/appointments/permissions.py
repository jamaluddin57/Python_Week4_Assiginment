from rest_framework.permissions import BasePermission

class IsAppointmentOwnerOrSuperuser(BasePermission):
    """
    Custom permission to allow only the doctor, patient, or superuser to view the appointment.
    Only superusers can update, delete, or create an appointment.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow viewing (GET) if the user is the doctor, patient, or superuser]
        print(obj)
        if request.method in ['GET']:
            return (
                request.user == obj.doctor or
                request.user == obj.patient or
                request.user.is_superuser
            )

        # Only superusers can perform updates, deletes, or create actions
        return request.user.is_superuser
