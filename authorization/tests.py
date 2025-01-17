from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from authorization.models import User


class AuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="TestPassword123!",  # nosec B106
            first_name="Test",
            last_name="User",
        )

        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

    def test_login_isSuccessful_whenCredentialsAreValid(self):
        # valid credentials
        response = self.client.post(
            self.login_url,
            {"email": "testuser@example.com", "password": "TestPassword123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["email"], "testuser@example.com")

    def test_login_fails_whenCredentialsAreInvalid(self):
        response = self.client.post(
            self.login_url,
            {"email": "testuser@example.com", "password": "WrongPassword!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_logout_isSuccessful_whenTokenIsValid(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.post(self.logout_url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Logout successful")
        self.assertFalse(Token.objects.filter(key=token.key).exists())

    def test_logout_fails_whenTokenIsInvalid(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalid_token")

        response = self.client.post(self.logout_url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_login_fails_whenPasswordIsMissing(self):
        response = self.client.post(
            self.login_url,
            {"email": "testuser@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_logout_fails_whenAuthorizationHeaderIsMissing(self):
        response = self.client.post(self.logout_url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
