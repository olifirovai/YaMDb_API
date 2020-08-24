from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Title, Genre, Review, Comment


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']


@admin.register(Title)
class TitleResource(ImportExportModelAdmin):
    list_display = ['name', 'year']
    search_fields = ['name']


@admin.register(Genre)
class GenreResource(ImportExportModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']


@admin.register(Review)
class ReviewResource(ImportExportModelAdmin):
    list_display = ['text', 'author']
    search_fields = ['text']


@admin.register(Comment)
class CommentResource(ImportExportModelAdmin):
    list_display = ['author', 'review', 'text']
    search_fields = ['author']
