from django.core.serializers import serialize
from rest_framework import serializers
import json

from rest_framework.permissions import AllowAny

from main.models import Habit_guide, Habit_user

from users.models import User, UserRoles


class UserSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "telegram_id", "password", "avatar", "phone", "country"]

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return User.objects.create_user(**validated_data)


class HabitGuideVSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit_guide
        fields = ["id", "action", "is_useful", "is_nice", "is_activ"]
        # validators = [lesson_linkValidator(field='lesson_link')]


class HabitUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit_user
        # Указываем поля, которые не должны отображаться
        # exclude = ('email', 'owner')
        fields = '__all__'
        # read_only_fields = ('email',)

    def get_user(self, instance):
        user = self.context['request'].user
        role = self.context['request'].user.role
        if role == UserRoles.MODERATOR:
            # Получаем сет объектов QuerySet
            response = instance.objects.all()
            # Сериализуем объкты QuerySet в формат Json
            serialized_data = serialize(
                "json", response, use_natural_foreign_keys=True)
            serialized_data = json.loads(serialized_data)
            return serialized_data
        else:
            # Получаем сет объектов QuerySet
            response = instance.objects.filter(owner=user).all()
            # Сериализуем объкты QuerySet в формат Json
            serialized_data = serialize(
                "json", response, use_natural_foreign_keys=True)
            serialized_data = json.loads(serialized_data)

            return serialized_data
