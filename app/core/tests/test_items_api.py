"""
Tests for the items API.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Item

from receipt.serializer import ItemSerializers


ITEMS_URL = reverse('receipt:item-list')


def create_user(email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicItemsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving items."""
        res = self.client.get(ITEMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateItemsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_items(self):
        """Test retrieving a list of items."""
        Item.objects.create(user=self.user, name='Kale', price=Decimal('1.23'))
        Item.objects.create(user=self.user, name='Vanilla', price=Decimal('0.45'))

        res = self.client.get(ITEMS_URL)

        items = Item.objects.all().order_by('-name')
        serializer = ItemSerializers(items, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_items_limited_to_user(self):
        """Test list of items is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Item.objects.create(user=user2, name='Salt', price=Decimal('0.99'))
        item = Item.objects.create(user=self.user, name='Pepper', price=Decimal('0.99'))

        res = self.client.get(ITEMS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], item.name)
        self.assertEqual(res.data[0]['id'], item.id)
