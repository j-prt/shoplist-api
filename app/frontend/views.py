"""
Views for HTML pages.
"""

from django.shortcuts import render
from django.views import generic
from django.urls import reverse, reverse_lazy  # noqa

from frontend import forms


def index(request):
    """View for the homepage."""
    return render(request, 'index.html')


class GoodbyeView(generic.TemplateView):
    template_name = 'goodbye.html'


class UserCreateView(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


# Create your views here.
