
from rest_framework import viewsets, generics, routers
from rest_framework.filters import SearchFilter, OrderingFilter
from django.urls import path, include
from rest_framework.permissions import IsAuthenticated, AllowAny

from main.models import habit_guide, Habit_user
from rest_framework.response import Response

# from main.paginators import MainPaginator
# from main.permissions import IsLessonOwner, IsModerator
from main.serializers import HabitGuideVSerializer, HabitUserSerializer
# from django.shortcuts import get_object_or_404

# from main.tasks_celery import send_email_confirmation
from users.models import UserRoles


class HabitGuideViewSet(viewsets.ModelViewSet):
    serializer_class = HabitGuideVSerializer
    queryset = habit_guide.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['well_name', 'payment_method']
    ordering_fields = ['date_of_payment']
    # permission_classes = [IsAuthenticated]




class HabitUserCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitUserSerializer
#     permission_classes = [IsAuthenticated]
#     read_only = True
#
#
#
class HabitUserListAPIView(generics.ListAPIView):
    serializer_class = HabitUserSerializer
    queryset = Habit_user.objects.all()
#     permission_classes = [AllowAny]
#     # permission_classes = [IsAuthenticated, IsModerator | IsLessonOwner]
#     pagination_class = MainPaginator
#
#     def get_queryset (self):
#         user=self.request.user
#         role=self.request.user.role
#         if role == UserRoles.MODERATOR:
#             return Lesson.objects.all()
#         else:
#             return Lesson.objects.filter(owner=user)
#
#
class HabitUserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitUserSerializer
    queryset = Habit_user.objects.all()
#     permission_classes = [IsAuthenticated, IsModerator | IsLessonOwner]
#
#
class HabitUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitUserSerializer
    queryset = Habit_user.objects.all()
#     permission_classes = [IsAuthenticated, IsModerator | IsLessonOwner]
#
#
#     def perform_update(self, serializer):
#         instance = serializer.save()
#         send_email_confirmation(lesson=instance.lesson_name, well_id=instance.well_name_id)
#

class HabitUserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitUserSerializer
    queryset = Habit_user.objects.all()
#     permission_classes = [IsAuthenticated, IsLessonOwner]
#
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