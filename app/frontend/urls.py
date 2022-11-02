"""
URL mappings for front end.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),

]
