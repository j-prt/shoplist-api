"""
Shopping list app serializers.
"""
from rest_framework import serializers

from core.models import (
    ShopList,
    Item,
    Category,
    Store,
)


class CatSerializer(serializers.ModelSerializer):
    """Serializer for category items."""

    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for store items."""

    class Meta:
        model = Store
        fields = ['id', 'name']
        read_only_fields = ['id']


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for list items."""
    category = CatSerializer(many=True, required=False)
    store = StoreSerializer(many=True, required=False)

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'category', 'store']
        read_only_fields = ['id']

    def _get_or_create_category(self, categories, instance):
        auth_user = self.context['request'].user
        for category in categories:
            cat_obj, created = Category.objects.get_or_create(
                user=auth_user,
                **category,
            )
            instance.category.add(cat_obj)

    def _get_or_create_store(self, stores, instance):
        auth_user = self.context['request'].user
        for store in stores:
            store_obj, created = Store.objects.get_or_create(
                user=auth_user,
                **store,
            )
            instance.store.add(store_obj)

    def update(self, instance, validated_data):
        """Update Item."""
        category = validated_data.pop('category', None)
        if category is not None:
            instance.category.clear()
            self._get_or_create_category(category, instance)
        store = validated_data.pop('store', None)
        if store is not None:
            instance.store.clear()
            self._get_or_create_store(store, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ShopListSerializer(serializers.ModelSerializer):
    """Serializer for shopping lists."""
    items = ItemSerializer

    class Meta:
        model = ShopList
        fields = ['id', 'title', 'items', 'total']
        read_only_fields = ['id']
