from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Profile
from django.core import mail

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword123',
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, self.user_data['email'])

    def test_create_profile_on_user_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.mobile_number, None)

class EmailVerificationTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword123',
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_send_verification_email(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('send_verification'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Email Verification", mail.outbox[0].subject)

    def test_verify_email_success(self):
        self.client.force_authenticate(user=self.user)
        verification_url = self.get_verification_url(self.user)

        response = self.client.get(verification_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_email_verified)

    def test_verify_email_invalid_token(self):
        verification_url = reverse('verify_email', kwargs={'uid': 'invalid_uid', 'token': 'invalid_token'})
        response = self.client.get(verification_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def get_verification_url(self, user):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import PasswordResetTokenGenerator
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        return reverse('verify_email', kwargs={'uid': uid, 'token': token})

class ProfileUpdateTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword123',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse('profile-update')

    def test_update_profile(self):
        data = {
            'mobile_number': '+1234567890',
            'instagram': 'https://instagram.com/testuser',
            'github': 'https://github.com/testuser',
        }
        response = self.client.patch(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.mobile_number, '+1234567890')
        self.assertEqual(self.user.profile.instagram, 'https://instagram.com/testuser')
        self.assertEqual(self.user.profile.github, 'https://github.com/testuser')

    def test_update_profile_unauthenticated(self):
        self.client.logout()  # Log out the user
        data = {
            'mobile_number': '+1234567890',
        }
        response = self.client.patch(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Expecting 401 for unauthorized access
