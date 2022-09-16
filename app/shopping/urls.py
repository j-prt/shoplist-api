"""
URL mappings for shopping list app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from shopping import views


router = DefaultRouter()
router.register('shopping', views.ShopListViewSet)

app_name = 'shopping'

urlpatterns = [
    path('', include(router.urls))
]
