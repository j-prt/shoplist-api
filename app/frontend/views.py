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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


class UserListsDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.ShopList
    template_name = 'lists_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


class ListCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = forms.ListCreateForm
    template_name = 'new_list.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form(self, form_class=form_class):
        form = super().get_form(form_class)
        form.fields['items'].queryset \
            = form.fields['items'].queryset.filter(user=self.request.user)
        return form


class DeleteListView(LoginRequiredMixin, generic.DeleteView):
    model = models.ShopList
    template_name = 'list_confirm_delete.html'
    success_url = reverse_lazy('user_lists')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class UserItemsView(LoginRequiredMixin, generic.ListView):
    model = models.Item
    template_name = 'user_items.html'
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ItemCreateView(LoginRequiredMixin, generic.CreateView):
    model = models.Item
    template_name = 'new_item.html'
    fields = ('name', 'price', 'category', 'store')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = 'Item name'
        form.fields['category'].label = 'Department'
        form.fields['category'].queryset \
            = form.fields['category'].queryset.filter(user=self.request.user)
        form.fields['store'].queryset \
            = form.fields['store'].queryset.filter(user=self.request.user)
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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


class ItemTagsView(LoginRequiredMixin, generic.ListView):
    template_name = 'user_tags.html'
    model = models.Category
    ordering = ['name']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'store_list': models.Store.objects
                                      .filter(user=self.request.user)
                                      .order_by('name'),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


class DeleteStoreView(LoginRequiredMixin, generic.DeleteView):
    model = models.Store
    template_name = 'store_confirm_delete.html'
    success_url = reverse_lazy('user_tags')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


class DeleteCategoryView(LoginRequiredMixin, generic.DeleteView):
    model = models.Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('user_tags')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


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
