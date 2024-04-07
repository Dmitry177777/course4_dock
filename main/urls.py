from django.urls import path

from main.apps import MainConfig
from rest_framework.routers import DefaultRouter

from main.views import (
    HabitGuideViewSet,
    UserCreateAPIView,
    HabitUserCreateAPIView,
    HabitUserListAPIView,
    HabitUserRetrieveAPIView,
    HabitUserUpdateAPIView,
    HabitUserDestroyAPIView, UserListAPIView, UserUpdateAPIView, UserDestroyAPIView
)

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'habit', HabitGuideViewSet, basename='habit')

urlpatterns = [
    path('user/create/',
         UserCreateAPIView.as_view(),
         name='user-create'),
    path('user/update/<int:pk>/',
         UserUpdateAPIView.as_view(),
         name='user-update'),
    path('user/delete/<int:pk>/',
         UserDestroyAPIView.as_view(),
         name='user-delete'),
    path('user/list/',
         UserListAPIView.as_view(),
         name='user-list'),

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
