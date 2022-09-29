from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import jwt

from .models import Order


class TestOrder(APITestCase):
    """
        docstring
    """

    def authenticate(self):
        """
            docstring
        """
        # Register a test user
        sample_user = {
            "mobile": "09123456789",
            "password": "123456",
            "confirm_password": "123456",
            "first_name": "test",
            "last_name": "user",
        }
        self.client.post(
            reverse("register-user"),
            sample_user
        )

        # Login with test user
        response = self.client.post(
            reverse("get-token"),
            sample_user
        )

        access_token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_register_order_without_authentication(self):
        """
            docstring
        """
        sample_order = {
            "address": "Client's Address",
            "description": "Client's Description",
        }
        response = self.client.post(
            reverse("register-order"),
            sample_order
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_order_with_authenticated_user(self):
        """
            docstring
        """
        # Register a test user
        self.authenticate()

        # Register an Order
        sample_order = {
            "address": "Client's Address",
            "description": "Client's Description",
        }
        response = self.client.post(
            reverse("register-order"),
            sample_order
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_orders(self):
        """
            docstring
        """

        # User Authentication
        self.authenticate()

        response = self.client.get(reverse("orders-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        # Register Test Order
        sample_order = {
            "address": "Client's Address",
            "description": "Client's Description",
        }
        response = self.client.post(
            reverse("register-order"),
            sample_order
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the User's Orders
        client = response.data["client"]
        client_orders = Order.objects.filter(client=client).count()
        self.assertEqual(client_orders, 1)
