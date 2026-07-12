from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверка, является ли пользователь модератором"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()


class IsOwner(BasePermission):
    """Проверка, является ли пользователь владельцем объекта"""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user