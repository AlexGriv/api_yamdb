from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class HasAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return request.user.role == 'admin'
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            if request.user.is_staff and request.data.get('role'):
                return False
            return request.user.role == 'admin'
        return False


class HasModeratorRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return request.user.role == 'moderator'
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return request.user.role == 'moderator'
        return False


class HasUserRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return request.user.role == 'user'
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated:
            return request.user.role == 'user'
        return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser
