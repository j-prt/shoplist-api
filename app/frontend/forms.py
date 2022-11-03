"""
Form classes for use on the front end.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from core import models


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('display_name', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['display_name'].label = 'Display name'
        self.fields['email'].label = 'Email address'
        self.fields['display_name'].widget.attrs['placeholder'] \
            = 'something cool'
        self.fields['email'].widget.attrs['placeholder'] \
            = 'something real'
        self.fields['password1'].widget.attrs['placeholder'] \
            = 'something secret'
        self.fields['password2'].widget.attrs['placeholder'] \
            = 'something secret again'

        self.fields['email'].widget.attrs['autofocus'] = False
        self.fields['display_name'].widget.attrs['autofocus'] = True

class ListCreateForm(forms.ModelForm):
    # items = forms.ModelMultipleChoiceField(models.Item.objects.all())
    class Meta:
        model = models.ShopList
        fields = ('title', 'items')
        widgets = {
            'items':forms.SelectMultiple(attrs={
                'class':'selectpicker',
                'data-live-search':'true',
                'data-style':'btn-primary',
                'data-selected-text-format':'count',
            }),
            'title':forms.TextInput(attrs={
                'class':'form-control',
                'style':'max-width: 270px;'
            }),
        }
