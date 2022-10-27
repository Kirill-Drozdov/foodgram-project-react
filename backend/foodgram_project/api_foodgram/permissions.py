from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnlyPermission(BasePermission):
    """
    Читать можно всем, остальное только админу.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and request.user.is_staff)


class IsStaffOrAuthorOrReadOnlyPermission(BasePermission):
    """
    Читать можно всем, добавлять авторизованным,
    остальное автору/админу.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user or request.user.is_staff)


class IsAdminOnlyPermission(BasePermission):
    """
    Доступ только администратору.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
