from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    message = 'Only an admin or owner can access this.'

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated():
            return request.user == obj.user
        else:
            return False