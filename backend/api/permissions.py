from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Разрешения для владельца."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class AuthorOrAdmins(permissions.BasePermission):
    """Разрешения для владельца и админов."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_admin)


class ReadOnly(permissions.BasePermission):
    """Разрешения для всех, только чтение."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
