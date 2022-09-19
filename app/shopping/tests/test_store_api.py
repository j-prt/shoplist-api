"""
Test the Store API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Store

from shopping.serializers import StoreSerializer


STORE_URL = reverse('shopping:store-list')


def detail_url(store_id):
    """Return store detail url."""
    return reverse('shopping:store-detail', args=[store_id])


def create_user(**params):
    """Create and return a user."""
    return get_user_model().objects.create_user(**params)


class PublicStoreAPITests(TestCase):
    """Test unauthenticated API access."""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test unauthenticated request returns error."""
        res = self.client.get(STORE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStoreAPITests(TestCase):
    """Test authenticated API access."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='passs')
        self.client.force_authenticate(self.user)

    def test_get_store_list(self):
        """Test retrieving list of stores."""
        Store.objects.create(user=self.user, name='Sears')
        Store.objects.create(user=self.user, name='Target')

        res = self.client.get(STORE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        stores = Store.objects.filter(user=self.user).order_by('-name')
        serializer = StoreSerializer(stores, many=True)
        self.assertEqual(res.data, serializer.data)
