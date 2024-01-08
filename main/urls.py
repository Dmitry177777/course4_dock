from django.urls import path

from main.apps import MainConfig
from rest_framework.routers import DefaultRouter

from main.views import (
    HabitGuideViewSet,
    HabitUserCreateAPIView,
    HabitUserListAPIView,
    HabitUserRetrieveAPIView,
    HabitUserUpdateAPIView,
    HabitUserDestroyAPIView
)

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'Habit', HabitGuideViewSet, basename='habit')


urlpatterns = [
    path('habit_user/create/',
         HabitUserCreateAPIView.as_view(),
         name='habit_user-create'),
    path('habit_user/',
         HabitUserListAPIView.as_view(),
         name='habit_user-list'),
    path('habit_user/<int:pk>/',
         HabitUserRetrieveAPIView.as_view(),
         name='habit_user-get'),
    path('habit_user/update/<int:pk>/',
         HabitUserUpdateAPIView.as_view(),
         name='habit_user-update'),
    path('habit_user/delete/<int:pk>/',
         HabitUserDestroyAPIView.as_view(),
         name='habit_user-delete'),

   ]+router.urls
