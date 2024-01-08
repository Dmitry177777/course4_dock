
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from main.models import Habit_guide, Habit_user

from main.paginators import MainPaginator
from main.permissions import IsModerator, IsHabitUserOwner

from main.serializers import HabitGuideVSerializer, HabitUserSerializer
from main.tasks_celery import send_telegram_confirmation

from users.models import UserRoles


class HabitGuideViewSet(viewsets.ModelViewSet):
    serializer_class = HabitGuideVSerializer
    queryset = Habit_guide.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['is_useful', 'is_nice']
    ordering_fields = ['action']
    # permission_classes = [IsAuthenticated]


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
