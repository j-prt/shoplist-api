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
        read_only_fields = ['id', 'private']


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for store items."""

    class Meta:
        model = Store
        fields = ['id', 'name']
        read_only_fields = ['id', 'private']


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for list items."""
    category = CatSerializer(many=False, required=False)
    store = StoreSerializer(many=False, required=False)

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'category', 'store']
        read_only_fields = ['id']

    def _get_or_create_category(self, category, instance):
        auth_user = self.context['request'].user
        cat_obj, created = Category.objects.get_or_create(
            user=auth_user,
            **category,
        )
        instance.category = cat_obj

    def _get_or_create_store(self, store, instance):
        auth_user = self.context['request'].user
        store_obj, created = Store.objects.get_or_create(
            user=auth_user,
            **store,
        )
        instance.store = store_obj

    def create(self, validated_data):
        """Create an item."""
        category = validated_data.pop('category', None)
        store = validated_data.pop('store', None)
        item = Item.objects.create(**validated_data)
        if category:
            self._get_or_create_category(category, item)
        if store:
            self._get_or_create_store(store, item)

        return item

    def update(self, instance, validated_data):
        """Update Item."""
        category = validated_data.pop('category', None)
        if category is not None:
            if instance.category:
                instance.category.delete()
            self._get_or_create_category(category, instance)
        store = validated_data.pop('store', None)
        if store is not None:
            if instance.store:
                instance.store.delete()
            self._get_or_create_store(store, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ShopListSerializer(serializers.ModelSerializer):
    """Serializer for shopping lists."""
    items = ItemSerializer(many=True, required=False)

    class Meta:
        model = ShopList
        fields = ['id', 'title', 'items', 'total']
        read_only_fields = ['id']

    def _get_or_create_items(self, items, instance):
        auth_user = self.context['request'].user
        for item in items:
            category = item.pop('category', None)
            store = item.pop('store', None)
            item_obj, created = Item.objects.get_or_create(
                user=auth_user,
                **item,
            )
            if category is not None:
                if item_obj.category:
                    item_obj.category.delete()
                cat_obj, created = Category.objects.get_or_create(
                    user=auth_user,
                    **category,
                )
                item_obj.category.add(cat_obj)
            if store is not None:
                if item_obj.store:
                    item_obj.store.delete()
                store_obj, created = Store.objects.get_or_create(
                    user=auth_user,
                    **store,
                )
                item_obj.store.add(store_obj)
            instance.items.add(item_obj)

    def create(self, validated_data):
        """Create a shopping list."""
        items = validated_data.pop('items', [])
        sl = ShopList.objects.create(**validated_data)
        self._get_or_create_items(items, sl)

        return sl

    def update(self, instance, validated_data):
        """Update shopping list."""
        items = validated_data.pop('items', None)
        if items is not None:
            instance.items.clear()
            self._get_or_create_items(items, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
