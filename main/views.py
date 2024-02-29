from django.core.serializers import serialize
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.utils import json

from main.models import Habit_guide, Habit_user, User

from main.paginators import MainPaginator
from main.permissions import IsModerator, IsHabitUserOwner

from main.serializers import HabitGuideVSerializer, HabitUserSerializer, UserSerializer
from main.tasks_celery import send_telegram_confirmation

from users.models import UserRoles
from rest_framework.response import Response
from rest_framework import status


class UserCreateAPIView(generics.CreateAPIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


    # отфильтровать набор запросов, чтобы гарантировать, что возвращаются только результаты, относящиеся к текущему аутентифицированному пользователю, делающему запрос.
    # def get_user(self):
    #     return User.objects.get(pk=self.request.user.pk)


    # def get_user(self, instance):
    #     user = self.context['request'].user
    #
    #     # Получаем сет объектов QuerySet
    #     response = instance.objects.filter(owner=user).all()
    #     # Сериализуем объкты QuerySet в формат Json
    #     serialized_data = serialize(
    #         "json", response, use_natural_foreign_keys=True)
    #     serialized_data = json.loads(serialized_data)
    #     return serialized_data
    #     # return User.objects.get(pk=self.request.user.pk)


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MainPaginator

    # отфильтровать набор запросов, чтобы гарантировать, что возвращаются только результаты, относящиеся к текущему аутентифицированному пользователю, делающему запрос.
    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk).all()


class HabitGuideViewSet(viewsets.ModelViewSet):
    serializer_class = HabitGuideVSerializer
    queryset = Habit_guide.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['is_useful', 'is_nice']
    ordering_fields = ['action']
    permission_classes = [IsAuthenticated]


class HabitUserCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitUserSerializer
    permission_classes = [IsAuthenticated]
    # read_only = True

    def perform_create(self, serializer):
        # Get the currently authenticated user
        user_instance = self.request.user

        # Create a 'Habit_user' instance with the
        # 'email' field associated with the user
        serializer.save(email=user_instance)
        send_telegram_confirmation(user_instance)


class HabitUserListAPIView(generics.ListAPIView):
    serializer_class = HabitUserSerializer
    read_only = True
    queryset = Habit_user.objects.all()
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated, IsModerator | IsHabitUserOwner]
    pagination_class = MainPaginator

    def get_queryset(self):
        user = self.request.user
        role = self.request.user.role
        if role == UserRoles.MODERATOR:
            return Habit_user.objects.filter(is_public=True)
        else:
            return Habit_user.objects.filter(email=user)


class HabitUserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitUserSerializer
    queryset = Habit_user.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsHabitUserOwner]


class HabitUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitUserSerializer
    queryset = Habit_user.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsHabitUserOwner]



#

#
#     def perform_update(self, serializer):
#         instance = serializer.save()
#         send_email_confirmation(
#         lesson=instance.lesson_name, well_id=instance.well_name_id)


class HabitUserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitUserSerializer
    queryset = Habit_user.objects.all()
    permission_classes = [IsAuthenticated, IsHabitUserOwner]

#
#
#
# class SubscriptionCreateAPIView(generics.CreateAPIView):
#     serializer_class = SubscriptionSerializer
#     permission_classes = [IsAuthenticated]
#
#
# class SubscriptionListAPIView(generics.ListAPIView):
#     serializer_class = SubscriptionSerializer
#     queryset = Subscription.objects.all()
#     permission_classes = [IsAuthenticated, IsModerator | IsLessonOwner]
#
#     def get_queryset (self):
#         user=self.request.user
#         role=self.request.user.role
#         if role == UserRoles.MODERATOR:
#             return Subscription.objects.all()
#         else:
#             return Subscription.objects.filter(owner=user)
#
#
# class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
#     serializer_class = SubscriptionSerializer
#     queryset = Subscription.objects.all()
#     permission_classes = [IsAuthenticated, IsModerator | IsLessonOwner]
#
#
#
# class SubscriptionUpdateAPIView(generics.UpdateAPIView):
#     serializer_class = SubscriptionSerializer
#     queryset = Subscription.objects.all()
#     permission_classes = [IsAuthenticated, IsModerator | IsLessonOwner]
# class SubscriptionDestroyAPIView(generics.DestroyAPIView):
#     queryset = Subscription.objects.all()
#     permission_classes = [IsAuthenticated, IsLessonOwner]
