from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Authenticates an admin user"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
