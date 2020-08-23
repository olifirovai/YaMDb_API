from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Title, Genre, Review, Comment, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'role', 'last_login', 'date_joined',)
    list_filter = ('last_login', 'date_joined',)
    readonly_fields = ['last_login', 'date_joined', ]
    empty_value_display = '-empty-'


admin.site.register(User, UserAdmin)


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
