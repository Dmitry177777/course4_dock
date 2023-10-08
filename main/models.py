from datetime import date, timedelta
from users.models import User, NULLABLE
import schedule
from django.core.mail import EmailMessage
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
# from django.utils.text import slugify
from pytils.translit import slugify

# NULLABLE = {'blank':True, 'null': True}


class Habit_guide (models.Model):
    objects = None
    action = models.TextField(max_length=1000, verbose_name='действие', unique=True, **NULLABLE)
    is_useful = models.BooleanField(default=False, verbose_name='признак полезной привычки')
    is_nice = models.BooleanField(default=False, verbose_name='признак приятной привычки')


    is_activ = models.BooleanField(default=True, verbose_name='признак активной привычки')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'{self.action}: {self.is_useful}: {self.is_nice}'


    def delete(self, *args, **kwargs):
        self.is_activ = False
        self.save()



class Habit_user(models.Model):
    objects = None
    email = models.ForeignKey(User, on_delete=models.CASCADE,  default='mail', verbose_name='почта_пользователя')
    place = models.CharField(max_length=150,  unique=True, default='', verbose_name='место')
    date_of_habit = models.DateTimeField(**NULLABLE, verbose_name='время выполнения привычки')

    action = models.ForeignKey(Habit_guide, to_field='action', on_delete=models.CASCADE,  verbose_name='действие', **NULLABLE)
    associated_action = models.ForeignKey(Habit_guide, to_field='action', related_name='associated_action', on_delete=models.CASCADE,  verbose_name='связанное действие', **NULLABLE)

    periodicity = models.DurationField(verbose_name='Периодичность' )
    reward = models.CharField(max_length=150,  verbose_name='Вознаграждение', **NULLABLE)
    time_to_complete = models.DurationField(**NULLABLE, verbose_name='время на выполнение привычки')

    is_public = models.BooleanField (default=False, verbose_name='признак публичной привычки')
    is_activ = models.BooleanField(default=True, verbose_name='признак активной привычки')

    class Meta:
        verbose_name = 'Моя привычка'
        verbose_name_plural = 'Мои привычки'

    def __str__(self):
        return f'{self.email}: {self.action}'



    #валилдация на уровне модели
    def clean(self):
        # У приятной привычки не может быть вознаграждения или связанной привычки.

        # Получите значение поля связанной модели
        related_field_value = self.habit_guide.is_nice
        if related_field_value is not None:
            if self.associated_action is not None or self.reward is not None:
                raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")

        else:
            # В связанные привычки могут попадать только привычки с признаком приятной привычки.
            if self.associated_action is not None:
                raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки")
            # Исключить одновременный выбор связанной привычки и указания вознаграждения.
            if self.associated_action is not None and self.reward is not None:
                raise ValidationError("Нужно выбрать либо вознаграждение, либо связанную привычку")

        # Время выполнения должно быть не больше 120 секунд.
        two_minutes = timedelta(minutes=2)
        if self.time_to_complete > two_minutes:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд")
        # Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
        one_week = timedelta(days=7)
        if self.periodicity < one_week:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней")


    def save(self, *args, **kwargs):
        self.clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)



    def delete(self, *args, **kwargs):
        self.is_activ = False
        self.save()

