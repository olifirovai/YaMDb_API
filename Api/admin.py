from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import Category, Title, Genre, Review, Comment, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'role', 'last_login', 'date_joined',)
    list_filter = ('last_login', 'date_joined',)
    readonly_fields = ['last_login', 'date_joined', ]
    empty_value_display = '-empty-'


admin.site.register(User, UserAdmin)


@admin.register(Category)
class CategoryResource(ImportExportModelAdmin):
    pass


@admin.register(Title)
class CategoryResource(ImportExportModelAdmin):
    pass


@admin.register(Genre)
class CategoryResource(ImportExportModelAdmin):
    pass


@admin.register(Review)
class CategoryResource(ImportExportModelAdmin):
    pass


@admin.register(Comment)
class CategoryResource(ImportExportModelAdmin):
    pass
