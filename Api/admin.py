
from django.contrib import admin

from Api.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'description', 'last_login', 'date_joined',)
    list_filter = ('last_login', 'date_joined',)
    readonly_fields = ['last_login', 'date_joined',]
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)