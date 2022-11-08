"""
Database models.
"""
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class NameField(models.CharField):
    """CharField that converts contents to title-case."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).title()


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    display_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class ShopList(models.Model):
    """Shopping list object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shoplists',
    )
    title = models.CharField(max_length=64, blank=True)
    items = models.ManyToManyField('Item', blank=True)
    active = models.BooleanField('Active', default=True)

    @property
    def total(self):
        return sum([item.price for item in self.items.all()])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.title:
            self.title = f'ShopList{self.id}'
            self.save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'lists_detail',
            kwargs={'pk': self.pk, 'slug': self.title}
        )

    def __str__(self):
        return self.title


class Item(models.Model):
    """Item object."""
    name = NameField(max_length=64)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='items',
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    store = models.ForeignKey(
        'Store',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user_items')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'],
                                    name='unique_item'),
        ]


class Category(models.Model):
    """Item category object."""
    name = NameField(max_length=64)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
    )
    private = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'],
                                    name='unique_category'),
        ]


class Store(models.Model):
    """Store object."""
    name = NameField(max_length=64)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stores',
    )
    private = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'],
                                    name='unique_store'),
        ]
