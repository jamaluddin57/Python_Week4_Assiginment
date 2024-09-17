from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.users.models import User
from rest_framework import status

class RegisterViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client = APIClient()

    def test_register_patient_as_admin(self):
        """
        Test registering a new patient by an admin user.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse('auth_register', kwargs={'user_type': 'patient'})  # Passing 'patient' as user_type
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.role, User.PATIENT)

    def test_register_doctor_as_admin_with_specialization(self):
        """
        Test registering a new doctor by an admin user with specialization.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse('auth_register', kwargs={'user_type': 'doctor'})  # Passing 'doctor' as user_type
        data = {
            'username': 'newdoctor',
            'email': 'newdoctor@test.com',
            'password': 'newpassword',
            'specialization': 'Cardiology',  # Specialization for doctors
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newdoctor').exists())
        new_user = User.objects.get(username='newdoctor')
        self.assertEqual(new_user.role, User.DOCTOR)
        self.assertEqual(new_user.specialization, 'Cardiology')


    def test_register_user_as_non_admin(self):
        """
        Test that a non-admin user cannot register a new user.
        """
        url = reverse('auth_register', kwargs={'user_type': 'patient'})
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_register_user_with_invalid_user_type(self):
        """
        Test that providing an invalid user_type in the URL results in an error.
        """
        self.client.force_authenticate(user=self.admin)
        url = reverse('auth_register', kwargs={'user_type': 'invalid_type'})  # Invalid user_type
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid user type provided', str(response.data))
