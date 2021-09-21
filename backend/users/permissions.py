from rest_framework import permissions


class AuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' and request.user.is_authenticated:
            return True
        return False
