from django.db import models
from api.users.models import User
from django.utils import timezone

class Appointment(models.Model):
    doctor = models.ForeignKey(User, related_name="doctor_appointment",on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name="patient_appointment", on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed= models.BooleanField(default=False)
    class Meta:
        unique_together = ('doctor','scheduled_at')
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        indexes = [
            models.Index(fields=['doctor']),
            models.Index(fields=['patient']),
        ]

    def __str__(self):
        return f"Appointment for {self.patient.get_full_name()} with Dr. {self.doctor.get_full_name()} on {self.scheduled_at}"