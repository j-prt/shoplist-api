"""
Views for HTML pages.
"""

from django.shortcuts import render
from django.views import generic


def index(request):
    """View for the homepage."""
    return render(request, 'index.html')

class GoodbyeView(generic.TemplateView):
    template_name = 'goodbye.html'



# Create your views here.
