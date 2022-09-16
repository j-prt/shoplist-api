"""
Test shopping list APIs.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    ShopList
)

from shopping.serializers import ShopListSerializer


LIST_URL = reverse('shopping:shoplist-list')


class PublicAPITests(TestCase):
    """Test unauthenticated API access."""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test authentication is required."""
        res = self.client.get(LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateAPITests(TestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='user1@example.com',
            password='passywordy',
        )
        self.client.force_authenticate(self.user)

    def test_get_shoplists(self):
        """Test retrieving shopping lists."""
        sl = ShopList.objects.create(user=self.user, title='Groceries')
        sl2 = ShopList.objects.create(user=self.user, title='Supplies')

        res = self.client.get(LIST_URL)

        slist = ShopList.objects.all().order_by('-id')
        serializer = ShopListSerializer(slist, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
