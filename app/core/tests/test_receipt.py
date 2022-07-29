"""
Tests for receipt APIs.
"""
from decimal import Decimal
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Receipt

from receipt.serializer import ReceiptSerializers


RECEIPT_URL = reverse('receipt:receipt-list')


def create_receipt(user, **params):
    """Create and return a sample receipt."""
    defaults = {
        'date_received': date.today(),
        'total': Decimal('125.21'),
        'store': 'Walmart'
    }
    defaults.update(params)

    receipt = Receipt.objects.create(user=user, **defaults)
    return receipt


class PublicReceiptAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RECEIPT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReceiptApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_receipts(self):
        """Test retrieving a list of receipts."""
        create_receipt(user=self.user)
        create_receipt(user=self.user)

        res = self.client.get(RECEIPT_URL)

        receipts = Receipt.objects.all().order_by('-id')
        serializer = ReceiptSerializers(receipts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_receipt_list_limited_to_user(self):
        """Test list of receipts is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_receipt(user=other_user)
        create_receipt(user=self.user)

        res = self.client.get(RECEIPT_URL)

        receipts = Receipt.objects.filter(user=self.user)
        serializer = ReceiptSerializers(receipts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)