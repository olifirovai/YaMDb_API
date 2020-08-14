from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime


class UserRole(models.Model):
    '''
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    '''

    ADMIN = 1
    MODERATOR = 2
    USER = 3

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,
                                          primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractUser):
    '''
    Creating the custom User model
    based on the AbstractUser model
    '''

    bio = models.TextField(max_length=200, blank=True,
                           verbose_name='user\'s biography', help_text='')
    role = models.ManyToManyField(UserRole, max_length=40, verbose_name='user\'s role')
    confirmation_code = models.CharField(max_length=30, unique=True)

    class Meta(AbstractUser.Meta):
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
        help_texts = {
            'bio': 'Shouldn\'t be more than 200 characters.',
            'role': '--------',
        }

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='category\'s name')
    slug = models.SlugField(unique=True, verbose_name='category\'s slug')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        help_texts = {
            'name': '----------',
            'slug': '--------',
        }

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='genre\'s name')
    slug = models.SlugField(unique=True, verbose_name='genre\'s slug')

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']
        help_texts = {
            'name': '----------',
            'slug': '--------',
        }

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=300, verbose_name='title\'s name')
    year = models.IntegerField(validators=[MinValueValidator(1894),
                                           MaxValueValidator(
                                               datetime.now().year)],
                               null=True, blank=True,
                               verbose_name='title\'s year')
    description = models.CharField(max_length=1000, blank=True,
                                   verbose_name='title\'s description')
    rating = models.IntegerField(blank=True, null=True,
                                 verbose_name='title\'s rating')
    genre = models.ManyToManyField(Genre, verbose_name='title\'s genre')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True,
                                 verbose_name='title\'s genre')

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'
        ordering = ['name']
        help_texts = {
            'name': '----------',
            'year': 'Use the following format: <YYYY>',
            'description': '----------',
            'rating': '--------',
            'genre': '----------',
            'category': '--------',
        }


class Review(models.Model):
    text = models.TextField(max_length=3000, verbose_name='review\'s text')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='review\'s author')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='review\'s score')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='review\'s date of publication')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='review\'s title')

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-pub_date']
        help_texts = {
            'text': '----------',
            'score': '--------',
            'title': '----------',
        }


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
        help_texts = {
            'text': '----------',
        }
