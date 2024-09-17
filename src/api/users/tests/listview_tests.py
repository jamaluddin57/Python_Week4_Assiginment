from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.users.models import User
from rest_framework import status

class UserListViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.doctor = User.objects.create_user('doctor', 'doctor@test.com', 'password')
        self.patient = User.objects.create_user('patient', 'patient@test.com', 'password')
        self.extra_doctor = User.objects.create_user('extra_doctor', 'extra_doctor@test.com', 'password')
        self.extra_patient = User.objects.create_user('extra_patient', 'extra_patient@test.com', 'password')
        self.doctor.role = User.DOCTOR
        self.patient.role = User.PATIENT
        self.extra_doctor.role = User.DOCTOR
        self.extra_patient.role = User.PATIENT
        self.doctor.save()
        self.patient.save()
        self.extra_doctor.save()
        self.extra_patient.save()
        self.client = APIClient()

    def test_list_users_as_admin_with_pagination(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-list', kwargs={'user_type': 'doctor'}) + '?page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Adjust based on pagination settings

    def test_list_users_as_non_admin_with_pagination(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('user-list', kwargs={'user_type': 'doctor'}) + '?page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_with_invalid_role(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-list', kwargs={'user_type': 'invalid_role'}) + '?page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
