from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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

    class Meta(AbstractUser.Meta):
        AbstractUser._meta.get_field('first_name').max_length = 20
        AbstractUser._meta.get_field('last_name').max_length = 40
        ordering = ['id']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=300)
    year = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    rating = models.IntegerField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True)

    class Meta:
        ordering = ['name']


class Review(models.Model):
    text = models.TextField(max_length=3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name="comments")
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
