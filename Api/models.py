from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser):
    description = models.TextField(max_length=120, blank=True, null=True)
    role = models



    class Meta(AbstractUser.Meta):
        AbstractUser._meta.get_field('first_name').max_length = 20
        AbstractUser._meta.get_field('last_name').max_length = 40
        AbstractUser._meta.get_field('email').required = True
        AbstractUser._meta.get_field('email').blank = False

    def __str__(self):
        return self.username
