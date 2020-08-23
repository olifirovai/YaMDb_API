from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserRole(models.TextChoices):
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''

    ADMIN = ('admin', 'admin',)
    MODERATOR = ('moderator', 'moderator',)
    USER = ('user', 'user',)


class User(AbstractUser):
    '''
    Creating the custom User model
    based on the AbstractUser model
    '''

    bio = models.TextField(max_length=200, blank=True,
                           verbose_name='user\'s biography',
                           help_text='Here You can add information about Youself')
    role = models.CharField(choices=UserRole.choices, default=UserRole.USER,
                            max_length=40, verbose_name='user\'s role')

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_staff or self.is_superuser

    class Meta(AbstractUser.Meta):
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='category\'s name')
    slug = models.SlugField(unique=True, verbose_name='category\'s slug',
                            help_text='This field should be unique')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='genre\'s name')
    slug = models.SlugField(unique=True, verbose_name='genre\'s slug',
                            help_text='This field should be unique')

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=300, verbose_name='title\'s name')
    year = models.IntegerField(validators=[MinValueValidator(1894),
                                           MaxValueValidator(
                                               datetime.now().year)],
                               null=True, blank=True,
                               verbose_name='title\'s year',
                               help_text='Should be XXXX type')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 related_name='category_titles', null=True,
                                 verbose_name='category')
    genre = models.ManyToManyField(Genre, related_name='genre_titles',
                                   blank=True, verbose_name='genre')
    description = models.TextField(blank=True,
                                   verbose_name='title description',
                                   help_text='Here you can add description about a movie')

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'
        ordering = ['name']


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='titles_reviews')
    text = models.TextField(verbose_name='review text')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_reviews',
                               verbose_name='review author')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='title score', help_text='Can range from 1 to 10')
    pub_date = models.DateTimeField(verbose_name='date published',
                                    auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-pub_date']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='comment\'s author')
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='review comment')
    text = models.TextField(verbose_name='comment\'s text')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='comment\'s date of publication')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-pub_date']
