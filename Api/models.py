from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class User(AbstractUser):
    bio = models.TextField(max_length=120, blank=True)
    role = models.CharField(max_length=20, blank=True, default='user')
    email = models.EmailField(blank=False, unique=True)


    class Meta(AbstractUser.Meta):
        AbstractUser._meta.get_field('first_name').max_length = 20
        AbstractUser._meta.get_field('last_name').max_length = 40

    def __str__(self):
        return self.username
