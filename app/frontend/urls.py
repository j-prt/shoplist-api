"""
URL mappings for front end.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('goodbye/', views.GoodbyeView.as_view(), name='goodbye'),
    path('signup/', views.UserCreateView.as_view(), name='signup'),
]
