from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from .models import Todo

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.register_url = '/api/user/register/'  # Example URL, adjust as needed
        self.user_data = {
            'username': 'testuser_1',  # Use a unique username for the setup
            'password': 'testpassword'
        }
        # Register a new user in setup
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Obtain token for the registered user
        response = self.client.post('/api/token/', {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.token = response.data.get('access')  # Adjust depending on your token structure
        self.assertIsNotNone(self.token, "Token was not generated")

    def test_user_registration_and_token(self):
        """Test user registration and token retrieval."""
        unique_username = 'testuser_2'  # Unique username
        user_data = {
            'username': unique_username,
            'password': 'testpassword',
        }
        
        response = self.client.post(self.register_url, user_data)
        
        # Print response data for debugging if the registration fails
        if response.status_code != status.HTTP_201_CREATED:
            print("User registration failed:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Obtain token for the registered user
        token_data = {
            'username': unique_username,
            'password': 'testpassword'
        }
        response = self.client.post('/api/token/', token_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if token is returned in response
        self.assertIn('access', response.data)

    def test_authenticated_access(self):
        """Test authenticated access with the user's token."""
        response = self.client.get('/api/todos/', 
                                    HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
