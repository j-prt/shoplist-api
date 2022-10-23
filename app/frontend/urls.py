"""
URL mappings for front end.
"""
from django.urls import (
    path,
    include,
)
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index')
]
