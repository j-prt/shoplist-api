"""
URL mappings for front end.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name="login.html"),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('goodbye/', views.GoodbyeView.as_view(), name='goodbye'),
    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('my_lists/', views.UserListsView.as_view(), name='user_lists'),
    path(
        'my_lists/<pk>/<slug>',
        views.UserListsDetailView.as_view(),
        name='lists_detail'
    ),
    path('new/', views.ListCreateView.as_view(), name='new_list'),
    path('my_items/', views.UserItemsView.as_view(), name='user_items'),
    path('new_item/', views.ItemCreateView.as_view(), name='new_item'),
    path(
        'my_items/delete/<pk>',
        views.DeleteItemView.as_view(),
        name='delete_item'
    ),
    path('my_tags/', views.ItemTagsView.as_view(), name='user_tags'),
    path(
        'store/delete/<pk>',
        views.DeleteStoreView.as_view(),
        name='delete_store'
    ),
    path(
        'dept/delete/<pk>',
        views.DeleteCategoryView.as_view(),
        name='delete_category'
    ),
    path('new_store/', views.StoreCreateView.as_view(), name='new_store'),
    path(
        'new_dept/',
        views.CategoryCreateView.as_view(),
        name='new_category'
    ),
]
