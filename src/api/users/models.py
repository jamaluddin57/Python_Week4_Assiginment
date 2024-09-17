from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404

class User(AbstractUser):
    # Define choices for the role field
    ADMIN = 'admin'
    PATIENT = 'patient'
    DOCTOR = 'doctor'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
    ]

    email = models.EmailField(unique=True, blank=False, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Role field with choices
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=PATIENT)

    def __str__(self):
        return self.username  # Use username or another field for the string representation

    def save(self, *args, **kwargs):
        # Automatically assign the 'admin' role if the user is a superuser
        if self.is_superuser:
            self.role = self.ADMIN
        super().save(*args, **kwargs)

    @classmethod
    def get_by_role(cls, role):
        return cls.objects.filter(role=role)

    @classmethod
    def get_by_id(cls, user_id):
        return get_object_or_404(cls, id=user_id)
