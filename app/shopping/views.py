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

from core.models import (
    ShopList
)

from shopping import serializers



class ShopListViewSet(viewsets.ModelViewSet):
    """Views for managing shopping list APIs."""
    serializer_class = serializers.ShopListSerializer
    queryset = ShopList.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve list of ingredients."""
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new shopping list."""
        serializer.save(user=self.request.user)
