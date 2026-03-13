from django.contrib.auth.models import User
from django.test import TestCase, Client
# from .models import DataStore
from api.models import CustomUser

class MyModelTests(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client()
        self.username = 'user1'
        self.password = 'password1'
        # Create the user and save with set_password to ensure the password is hashed correctly
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)


    def test_api_events_access_should_succeed(self):
        # Use the test client to check a view
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, 200)


    def test_service_events_access_should_fail(self):
        # Use the test client to check a view
        response = self.client.get('/service/events/')
        self.assertEqual(response.status_code, 403)


    def test_login_with_correct_credentials(self):
        # Attempt to log in with the correct plain-text password
        login_successful = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login_successful, "Login should be successful with correct credentials")

        # You can now access views that require a logged-in user
        response = self.client.get('/service/events/')
        self.assertEqual(response.status_code, 200) # Check for a successful page load


    def test_login_with_invalid_credentials(self):
        # Attempt to log in with an incorrect password
        login_successful = self.client.login(username=self.username, password='wrongpassword')
        self.assertFalse(login_successful, "Login should fail with invalid credentials")

        # Check that an unauthenticated request is redirected to the login page
        response = self.client.get('/service/events/', follow=True)
        self.assertEqual(response.status_code, 403) # Check for a failed page load
        # The exact redirect URL depends on your project's settings (e.g., LOGIN_URL)
        # self.assertRedirects(response, '/accounts/login/?next=/some-protected-url/')
