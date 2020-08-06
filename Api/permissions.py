from rest_framework import permissions


class IsOwner(permissions.IsAuthenticated):
    message = 'Only an admin or an owner can access this.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.is_staff or request.user.is_superuser)


