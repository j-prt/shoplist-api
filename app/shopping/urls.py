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
router.register('list', views.ShopListViewSet)
router.register('item', views.ItemViewSet)
router.register('category', views.CatViewSet)
router.register('store', views.StoreViewSet)

app_name = 'shopping'

urlpatterns = [
    path('', include(router.urls))
]
