"""
Views for HTML pages.
"""

from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

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
        return queryset.filter(
            user_id=self.request.user.id
            ).order_by('-active', '-id')


class UserListsDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.ShopList
    template_name = 'lists_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        default_stores = {
            'Costco': 'assets/costco.jpg',
            'Freshco': 'assets/freshco.jpg',
            'Loblaws': 'assets/loblaws.jpg',
            'Petsmart': 'assets/petsmart.jpg',
            'Rcss': 'assets/rcss.jpg',
            'Safeway': 'assets/safeway.jpg',
            'Save-On-Foods': 'assets/saveon.jpg',
            'Walmart': 'assets/walmart.jpg',
            'None': None,
            }
        try:
            if self.object.items.all()[0].store.name in default_stores:
                first = self.object.items.all()[0].store.name
            else:
                first = 'None'
        except AttributeError:
            first = 'None'
        context.update({'img_url': default_stores[first]})
        return context


class ListCompleteView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            'lists_detail',
            kwargs={
                'pk': self.kwargs.get('pk'),
                'slug': self.kwargs.get('slug'),
                }
            )

    def get(self, request, *args, **kwargs):
        shoplist = models.ShopList.objects.get(id=self.kwargs.get('pk'))
        shoplist.active = not shoplist.active
        shoplist.save()

        return super().get(request, *args, **kwargs)


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


class ListEditView(LoginRequiredMixin, generic.UpdateView):
    model = models.ShopList
    form_class = forms.ListCreateForm
    template_name = 'list_edit.html'

    def get_form(self, form_class=form_class):
        form = super().get_form(form_class)
        form.fields['items'].queryset \
            = form.fields['items'].queryset.filter(user=self.request.user)
        return form

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


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
        form.fields['category'].label = 'Category'
        form.fields['category'].queryset \
            = form.fields['category'].queryset.filter(
                Q(user=self.request.user) | Q(private=False)
            ).order_by('name')
        form.fields['store'].queryset \
            = form.fields['store'].queryset.filter(
                Q(user=self.request.user) | Q(private=False)
            ).order_by('name')
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
                                      .filter(
                                        Q(user=self.request.user) |
                                        Q(private=False)
                                        ).order_by('name')
                                         .order_by('-private'),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(user=self.request.user) | Q(private=False)
        ).order_by('-private')


class DeleteStoreView(LoginRequiredMixin, generic.DeleteView):
    model = models.Store
    template_name = 'store_confirm_delete.html'
    success_url = reverse_lazy('user_tags')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


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
        form.fields['name'].label = 'Category name'
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


@login_required
def manage_token(request):
    context = {}

    if request.method == 'POST':
        try:
            Token.objects.get(user=request.user).delete()
            token = Token.objects.create(user=request.user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=request.user)
        context['token'] = token.key

    return render(request, 'manage_token.html', context=context)
