"""
Views for HTML pages.
"""

from django.shortcuts import render


def index(request):
    """This is a docstring"""
    return render(request, 'index.html', {})

# Create your views here.
