"""
Shopping list API views.
"""
from rest_framework import (
    viewsets,
    mixins,
    status
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import (
    ShopList,
    Item,
    Category,
    Store,
)

from shopping import serializers


class ShopListViewSet(viewsets.ModelViewSet):
    """Views for managing shopping list APIs."""
    serializer_class = serializers.ShopListSerializer
    queryset = ShopList.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve shopping list."""
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new shopping list."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='add-item')
    def add_item(self, request, pk=None):
        sl = self.get_object()
        auth_user = self.request.user

        for item in request.data['items']:
            item_obj, created = Item.objects.get_or_create(
                user=auth_user,
                **item,
            )
            sl.items.add(item_obj)

        sl.save()
        serializer = self.serializer_class(sl)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemViewSet(mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """Views for managing item APIs."""
    serializer_class = serializers.ItemSerializer
    queryset = Item.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve list of items."""
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-name')


class CatViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """Views for managing category APIs."""
    serializer_class = serializers.CatSerializer
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve list of categories."""
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-name')


class StoreViewSet(mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Views for managing store APIs."""
    serializer_class = serializers.StoreSerializer
    queryset = Store.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve list of stores."""
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-name')
