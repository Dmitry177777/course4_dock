from rest_framework.permissions import BasePermission
# import users
from users.models import UserRoles


class IsModerator(BasePermission):
    message = "Вы не являетесь модератором!"

    def has_object_permission(self, request, view, obj):
        if request.user.role == "MODERATOR":
            return True
        return False


class IsPublic(BasePermission):
    message = "Нет публичных привычек!"

    # def has_permission(self, request, view):
    #     return True

    def has_object_permission(self, request, view, obj):
        print(obj.is_public)
        return obj.is_public


class IsHabitUserOwner(BasePermission):
    message = "Вы не являетесь владельцем!"


    def has_object_permission(self, request, view, obj):
        if request.user == obj.email.email:
            return True
        return False
