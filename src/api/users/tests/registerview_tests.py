from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.users.models import User
from rest_framework import status

class RegisterViewTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client = APIClient()

    def test_register_user_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpassword',
            'role': User.PATIENT
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_as_non_admin(self):
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpassword',
            'role': User.PATIENT
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_user_with_missing_fields(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'password': 'newpassword'
            # Missing 'email' and 'role'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_with_invalid_role(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpassword',
            'role': 'invalid_role'  # Invalid role
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
