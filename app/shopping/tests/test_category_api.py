"""
Tests for category APIs.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category

from shopping.serializers import CatSerializer


CAT_URL = reverse('shopping:category-list')


def detail_url(cat_id):
    """Return category detail url"""
    return reverse('shopping:category-detail', args=[cat_id])


def create_user(**params):
    """Create and return a user."""
    return get_user_model().objects.create_user(**params)


class PublicItemAPITests(TestCase):
    """Test unauthenticated API access."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required."""
        res = self.client.get(CAT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateItemAPITests(TestCase):
    """Test authenticated API access."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='passs')
        self.client.force_authenticate(self.user)

    def test_get_categories(self):
        """Test retrieving categories."""
        Category.objects.create(user=self.user, name='foodstuff')
        Category.objects.create(user=self.user, name='laundry')

        res = self.client.get(CAT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        cats = Category.objects.filter(user=self.user).order_by('-name')
        serializer = CatSerializer(cats, many=True)
        self.assertEqual(res.data, serializer.data)
