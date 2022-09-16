"""
Shopping list app serializers.
"""
from rest_framework import serializers

from core.models import (
    ShopList
)


class ShopListSerializer(serializers.ModelSerializer):
    """Serializer for shopping lists."""

    class Meta:
        model = ShopList
        fields = ['id', 'title']
        read_only_fields = ['id']
