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


def detail_url(list_id):
    """Return shopping list detail url"""
    return reverse('shopping:shoplist-detail', args=[list_id])

def create_list(user, **params):
    """Create and return a list."""
    defaults = {
        'title': 'None',
    }
    defaults.update(params)

    sl = ShopList.objects.create(user=user, **defaults)
    return sl

def create_user(**params):
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(
            email='user1@example.com',
            password='passywordy',
        )
        self.client.force_authenticate(self.user)

    def test_get_shoplists(self):
        """Test retrieving shopping lists."""
        sl1 = ShopList.objects.create(user=self.user, title='Groceries')
        sl2 = ShopList.objects.create(user=self.user, title='Supplies')

        res = self.client.get(LIST_URL)

        slist = ShopList.objects.all().order_by('-id')
        serializer = ShopListSerializer(slist, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_shoplist(self):
        """Test creating a shopping list."""
        payload = {
            'title': 'stuff'
        }

        res = self.client.post(LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        slist = ShopList.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(slist, k), v)
        self.assertEqual(slist.user, self.user)

    def test_delete_shoplist(self):
        """Test deleting own shopping list."""
        sl = create_list(user=self.user)

        url = detail_url(sl.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ShopList.objects.filter(id=sl.id).exists())

    def test_delete_other_shoplist(self):
        """Test deleting other's shopping list."""
        user2 = create_user(email='user2@example.com', password='passs')
        sl = create_list(user=user2)

        url = detail_url(sl.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(ShopList.objects.filter(id=sl.id).exists)
