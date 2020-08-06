from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, **kwargs):
        user = self.model(email=email, username=username, **kwargs)
        user.save()
        return user

    def create_superuser(self, email, **kwargs):
        user = self.model(email=email, is_staff=True, is_superuser=True,
                          **kwargs)
        user.save()
        return user


class User(AbstractUser):
    USER_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    bio = models.TextField(max_length=120, blank=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    confirmation_code = models.CharField(max_length=30, unique=True)
    is_moderator = models.BooleanField(default=False)

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        AbstractUser._meta.get_field('first_name').max_length = 20
        AbstractUser._meta.get_field('last_name').max_length = 40

    def __str__(self):
        return self.username
