"""Populates default Stores and Categories"""
import sys
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from core.models import (
    Store,
    Category,
    User,
)


DEFAULT_STORES = [
    'Walmart',
    'Costco',
    'Superstore',
    'Loblaws',
    'Freshco',
    'Petsmart',
    'Save-On-Foods',
    'Safeway',

]

DEFAULT_CATEGORIES = [
    'Grocery',
    'Produce',
    'Chemicals',
    'Paper Gods',
    'Frozen',
    'Dairy',
    'Meats',
    'Deli',
    'Bakery',
    'Pharmacy',
    'Health & Beauty',
    'Pet Food',
    'Pet Treats',
    'Pet Supplies',
    'General Merchandise',
]


user, _ = User.objects.get_or_create(
    email='defaults@default.com',
    password='defaultpass123'
)


def populate_stores(user, stores):
    """Create default store objects."""

    sys.stdout.write('Populating stores..')
    try:
        for store in stores:
            Store.objects.create(user=user, name=store, private=False)
            sys.stdout.write('.')
    except IntegrityError:
        print('\nError: Default stores already exist.')
    sys.stdout.write('Complete!\n')


def populate_categories(user, categories):
    """Create default category objects."""

    sys.stdout.write('Populating categories..')
    try:
        for category in categories:
            Category.objects.create(user=user, name=category, private=False)
            sys.stdout.write('.')
    except IntegrityError:
        print('\nError: Default categories already exist.')
    sys.stdout.write('Complete!\n')


class Command(BaseCommand):
    """Django command to populate default tags."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        populate_stores(user, DEFAULT_STORES)
        populate_categories(user, DEFAULT_CATEGORIES)
