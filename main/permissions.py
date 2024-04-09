from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = "Вы не являетесь модератором!"

    def has_object_permission(self, request, view, obj):
        if request.user.role == "MODERATOR":
            return True
        return False


class IsHabitUserOwner(BasePermission):
    message = "Вы не являетесь владельцем!"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.email.email:
            return True
        return False
