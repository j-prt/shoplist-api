"""
Test the Item APIs.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from decimal import Decimal

from core.models import (
    Item,
    Category,
)

from shopping.serializers import ItemSerializer


ITEM_URL = reverse('shopping:item-list')


def detail_url(item_id):
    """Return item detail url."""
    return reverse('shopping:item-detail', args=[item_id])


def create_user(**params):
    """Create and return a user."""
    return get_user_model().objects.create_user(**params)


def create_item(user, **params):
    """Create and return an item."""
    defaults = {
        'name': 'bananas',
        'price': 2.50,
    }
    defaults.update(params)
    item = Item.objects.create(user=user, **defaults)
    return item


class PublicItemAPITests(TestCase):
    """Test unauthenticated API access."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test unauthenticated request returns error."""
        res = self.client.get(ITEM_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateItemAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='passs')
        self.client.force_authenticate(self.user)

    def test_get_item_list(self):
        """Test retrieving list of items."""
        create_item(user=self.user, name='ananas')
        create_item(user=self.user)

        res = self.client.get(ITEM_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        items = Item.objects.filter(user=self.user).order_by('-name')
        serializer = ItemSerializer(items, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_create_new_item(self):
        """Test creating an item."""
        payload = {'name': 'fish sticks', 'price': Decimal('9.99')}

        res = self.client.post(ITEM_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        item = Item.objects.get(user=self.user, name=payload['name'])
        for k, v in payload.items():
            if isinstance(v, str):
                self.assertEqual(getattr(item, k), v.title())
            else:
                self.assertEqual(getattr(item, k), v)

    def test_add_category_to_item(self):
        """Test adding category to existing item."""
        item = create_item(user=self.user)

        payload = {
            'category': {'name': 'Produce'}
        }

        url = detail_url(item.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        category = Category.objects.get(user=self.user, name='Produce')
        item.refresh_from_db()
        self.assertEqual(category, item.category)
