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


class ListCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ListCreateForm
    template_name = 'new_list.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UserItemsView(LoginRequiredMixin, generic.ListView):
    model = models.Item
    template_name = 'user_items.html'
    ordering = ['name']


class ItemCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Item
    template_name = 'new_item.html'
    fields = ('name', 'price', 'category', 'store')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = 'Item name'
        form.fields['category'].label = 'Department'
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeleteItemView(LoginRequiredMixin, generic.DeleteView):
    model = models.Item
    template_name = 'item_confirm_delete.html'
    success_url = reverse_lazy('user_items')


class ItemTagsView(LoginRequiredMixin, generic.ListView):
    template_name = 'user_tags.html'
    model = models.Category
    ordering = ['name']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'store_list': models.Store.objects.order_by('name'),
        })
        return context


class DeleteStoreView(LoginRequiredMixin, generic.DeleteView):
    model = models.Store
    template_name = 'store_confirm_delete.html'
    success_url = reverse_lazy('user_tags')


class DeleteCategoryView(LoginRequiredMixin, generic.DeleteView):
    model = models.Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('user_tags')


class StoreCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Store
    template_name = 'new_store.html'
    fields = ('name',)

    def get_success_url(self):
        return reverse('user_tags')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = 'Store name'
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Category
    template_name = 'new_category.html'
    fields = ('name',)

    def get_success_url(self):
        return reverse('user_tags')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = 'Department name'
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
