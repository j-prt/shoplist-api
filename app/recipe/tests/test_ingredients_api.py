"""
Tests for the ingredients API.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Ingredient,
    Recipe,
)

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """Get URL for ingredient details."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='user@example.com', password='testpass'):
    """Create and return user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredientsAPITests(TestCase):
    """Test unauthorized .API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authorization is required to make API requests."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving ingredients list."""
        Ingredient.objects.create(user=self.user, name='Paprika')
        Ingredient.objects.create(user=self.user, name='Balsamic')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredients = Ingredient.objects.all().order_by('-id')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test ingredients are limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Ingredient.objects.create(user=user2, name='Potato')
        ingredient = Ingredient.objects.create(user=self.user, name='Tomato')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating ingredient functionality."""
        ingredient = Ingredient.objects.create(user=self.user, name='Carrots')

        payload = {'name': 'Cabbage'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test deleting ingredient functionality."""
        ingredient = Ingredient.objects.create(user=self.user, name='Mayo')

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())

    def test_filter_ingredient_by_assigned(self):
        """Test filtering ingredients by recipe assignment"""
        in1 = Ingredient.objects.create(user=self.user, name='Potatoes')
        in2 = Ingredient.objects.create(user=self.user, name='Onions')
        in3 = Ingredient.objects.create(user=self.user, name='Watermelon')
        r1 = Recipe.objects.create(
            user=self.user,
            title='Stew',
            time_minutes=90,
            price=Decimal('8.50')
        )
        r1.ingredients.add(in1, in2)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        s1 = IngredientSerializer(in1)
        s2 = IngredientSerializer(in2)
        s3 = IngredientSerializer(in3)
        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)

    def test_filtered_ingredients_unique(self):
        """Test filtered ingredients list does not contain duplicates."""
        in1 = Ingredient.objects.create(user=self.user, name='Oregano')
        Ingredient.objects.create(user=self.user, name='Cherries')
        r1 = Recipe.objects.create(
            title='Pizza margherita',
            user=self.user,
            time_minutes=17,
            price=Decimal('11.21'),
        )
        r2 = Recipe.objects.create(
            title='Ossobuco',
            user=self.user,
            time_minutes=45,
            price=Decimal('27.30'),
        )
        r1.ingredients.add(in1)
        r2.ingredients.add(in1)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
