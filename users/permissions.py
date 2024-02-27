from rest_framework.permissions import BasePermission
from users.models import UserRoles


class IsModerator(BasePermission):
    message = "Ошибка! Вы не являетесь модератором!"

    def has_permission(self, request, view):
        return request.user.role == UserRoles.MODERATOR


class IsOwner(BasePermission):
    message = "Ошибка! Вы не являетесь автором!"

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
