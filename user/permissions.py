from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Only an Admin has permission for this action'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin))


class IsAdmin(permissions.BasePermission):
    message = 'Only an Admin has permission for this action'

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin)


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    message = 'an Admin, an Author or a Moderator have\
               permission for this action'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj=None):
        return (request.method in SAFE_METHODS or request.user.is_authenticated
                and (request.user.is_admin or request.user.is_moderator
                     or obj.author == request.user))
