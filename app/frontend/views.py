"""
Views for HTML pages.
"""

from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy  # noqa
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from frontend import forms
from core import models


User = get_user_model()


def index(request):
    """View for the homepage."""
    return render(request, 'index.html')


class GoodbyeView(generic.TemplateView):
    template_name = 'goodbye.html'


class UserCreateView(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class UserListsView(LoginRequiredMixin, generic.ListView):
    model = models.ShopList
    template_name = 'user_lists.html'
    ordering = ['-id']


class UserListsDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.ShopList
    template_name = 'lists_detail.html'



# Create your views here.
