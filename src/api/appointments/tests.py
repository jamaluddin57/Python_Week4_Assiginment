from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.appointments.models import Appointment
from api.users.models import User
from rest_framework import status
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

class AppointmentListViewTests(APITestCase):

    def setUp(self):
        # Set up users and appointments for testing
        self.superuser = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.doctor = User.objects.create_user('doctor', 'doctor@test.com', 'password')
        self.patient = User.objects.create_user('patient', 'patient@test.com', 'password')
        # Using timezone-aware datetime objects
        self.doctor.role = User.DOCTOR
        self.patient.role = User.PATIENT
        self.doctor.save()
        self.patient.save()
        self.appointment1 = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            scheduled_at=timezone.now(),  # Timezone-aware datetime
            is_completed=False
        )
        self.appointment2 = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            scheduled_at=timezone.now()+timedelta(hours=7),  # Timezone-aware datetime
            is_completed=True
        )

        self.client = APIClient()

    def test_list_appointments_as_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_appointments_as_doctor(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_appointments_as_patient(self):
        self.client.force_authenticate(user=self.patient)
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_appointments_unauthenticated(self):
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
   
    def test_list_appointments_with_filter(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('appointment-list') + '?is_completed=True'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_list_appointments_with_filter_as_doctor(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('appointment-list') + '?is_completed=True'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_list_appointments_with_filter_as_patient(self):
        self.client.force_authenticate(user=self.patient)
        url = reverse('appointment-list') + '?is_completed=True'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class AppointmentDetailViewTests(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin2', 'admin2@test.com', 'password')
        self.doctor = User.objects.create_user('doctor', 'doctor@test.com', 'password')
        self.patient = User.objects.create_user('patient', 'patient@test.com', 'password')
        self.other_user = User.objects.create_user('other', 'other@test.com', 'password')

        # Using timezone-aware datetime objects
        self.appointment = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            scheduled_at=timezone.now(),  # Timezone-aware datetime
            is_completed=False
        )
        self.client = APIClient()

    def test_retrieve_appointment_as_owner(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('appointment-detail', kwargs={'id': self.appointment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.appointment.id)

    def test_retrieve_appointment_as_non_owner(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('appointment-detail', kwargs={'id': self.appointment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_appointment_as_owner(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('appointment-detail', kwargs={'id': self.appointment.id})
        data = {'is_completed': True}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.appointment.refresh_from_db()
        self.assertFalse(self.appointment.is_completed)
    
    def test_update_appointment_as_superuser(self):
        self.superuser = User.objects.create_superuser('admin3', 'admin3@test.com', 'password')
        self.client.force_authenticate(user=self.superuser)
        url = reverse('appointment-detail', kwargs={'id': self.appointment.id})
        data = {'is_completed': True}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertTrue(self.appointment.is_completed)

    def test_delete_appointment_as_superuser(self):
        self.superuser = User.objects.create_superuser('admin4', 'admin4@test.com', 'password')
        self.client.force_authenticate(user=self.superuser)
        url = reverse('appointment-detail', kwargs={'id': self.appointment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_retrieve_non_existent_appointment(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('appointment-detail', kwargs={'id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_appointment_with_invalid_data(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('appointment-detail', kwargs={'id': self.appointment.id})
        data = {'is_completed': 'invalid_data'}  # Invalid data type
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_appointment_as_superuser(self):
        self.client.force_authenticate(user=self.superuser)
        data={'scheduled_at': timezone.now()}
        url = reverse('appointment-detail', kwargs={'id': self.appointment.id})
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    


class AppointmentReportViewTests(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.doctor = User.objects.create_user('doctor', 'doctor@test.com', 'password')
        self.patient = User.objects.create_user('patient', 'patient@test.com', 'password')
        self.patient.role=User.PATIENT
        self.doctor.role=User.DOCTOR
        self.patient.save()
        self.doctor.save()

        # Using timezone-aware datetime objects
        Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            scheduled_at=timezone.now(),  # Timezone-aware datetime
            is_completed=False
        )
        Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            scheduled_at=timezone.now()+timedelta(hours=6),  # Timezone-aware datetime
            is_completed=True
        )

        self.client = APIClient()

    def test_report_view(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('appointment-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data[0])
        self.assertIn('date', response.data[0])

    def test_report_view_as_non_superuser(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('appointment-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_report_view_with_invalid_date_range(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('appointment-report') + '?start_date=invalid_date&end_date=invalid_date'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class AppointmentCreateViewTests(APITestCase):

    def setUp(self):
        self.doctor = User.objects.create_user('doctor', 'doctor@test.com', 'password')
        self.patient = User.objects.create_user('patient', 'patient@test.com', 'password')
        self.superuser = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.doctor.role = User.DOCTOR
        self.doctor.save()
        self.client = APIClient()

    def test_create_appointment(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('appointment-create')
        data = {
            'doctor_id': self.doctor.id,
            'patient_id': self.patient.id,
            'scheduled_at': timezone.now()+timedelta(hours=10),  # Timezone-aware datetime
            'is_completed': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_create_appointment_unauthenticated(self):
        url = reverse('appointment-create')
        data = {
            'doctor': self.doctor.id,
            'patient': self.patient.id,
            'scheduled_at': timezone.now(),  # Timezone-aware datetime
            'is_completed': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_appointment_with_missing_required_fields(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('appointment-create')
        data = {
            'doctor_id': self.doctor.id,
            'scheduled_at': timezone.now()+timedelta(hours=20),  # Missing patient_id
            'is_completed': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

