from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.users.models import User
from rest_framework import status

class UserDetailViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.doctor = User.objects.create_user('doctor', 'doctor@test.com', 'password')
        self.patient = User.objects.create_user('patient', 'patient@test.com', 'password')
        self.doctor.role = User.DOCTOR
        self.patient.role = User.PATIENT
        self.doctor.save()
        self.patient.save()
        self.client = APIClient()

    def test_retrieve_user_as_owner(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('user-detail', kwargs={'id': self.doctor.id, 'user_type': 'doctor'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.doctor.id)

    def test_retrieve_user_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', kwargs={'id': self.doctor.id, 'user_type': 'doctor'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.doctor.id)

    def test_retrieve_user_as_non_owner_non_admin(self):
        self.client.force_authenticate(user=self.patient)
        url = reverse('user-detail', kwargs={'id': self.doctor.id, 'user_type': 'doctor'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_as_owner(self):
        self.client.force_authenticate(user=self.doctor)
        url = reverse('user-detail', kwargs={'id': self.doctor.id, 'user_type': 'doctor'})
        data = {'email': 'newemail@test.com'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_as_admin_with_existing_email(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', kwargs={'id': self.doctor.id, 'user_type': 'doctor'})
        data = {'email': 'admin@test.com'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', kwargs={'id': self.doctor.id, 'user_type': 'doctor'})
        data = {'email': 'newemail@test.com'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.email, 'newemail@test.com')

    def test_delete_user_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', kwargs={'id': self.doctor.id, 'user_type': 'doctor'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.doctor.id).exists())

    def test_delete_user_as_non_admin(self):
        self.client.force_authenticate(user=self.patient)
        url = reverse('user-detail', kwargs={'id': self.doctor.id, 'user_type': 'doctor'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_with_invalid_id(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', kwargs={'id': 9999, 'user_type': 'doctor'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
