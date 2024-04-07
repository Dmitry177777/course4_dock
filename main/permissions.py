from rest_framework.permissions import BasePermission, SAFE_METHODS

import users
from users.models import UserRoles


class IsModerator(BasePermission):
    message = "Вы не являетесь модератором!"

    def has_permission(self, request, view):
        if request.user.role == "MODERATOR":
            return True
        return False


class IsHabitUserOwner(BasePermission):
    message = "Вы не являетесь владельцем!"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.email:
            return True
        return False



