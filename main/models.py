from datetime import date
from users.models import User, NULLABLE
import schedule
from django.core.mail import EmailMessage
from django.db import models
from django.urls import reverse

# from django.utils.text import slugify
from pytils.translit import slugify

# NULLABLE = {'blank':True, 'null': True}


class habit_guide (models.Model):
    objects = None
    action = models.TextField(max_length=1000, verbose_name='действие', unique=True, **NULLABLE)
    is_nice = models.BooleanField(default=True, verbose_name='признак приятной привычки')
    is_useful = models.BooleanField(default=True, verbose_name='признак полезной привычки')

    is_activ = models.BooleanField(default=True, verbose_name='признак активной привычки')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'{self.action}: {self.is_nice}: {self.is_useful}'


    def delete(self, *args, **kwargs):
        self.is_activ = False
        self.save()


class habit_associated (models.Model):
    objects = None
    associated_action = models.TextField(max_length=1000, verbose_name='связанное действие', unique=True, **NULLABLE)

    is_activ = models.BooleanField(default=True, verbose_name='признак активной привычки')

    class Meta:
        verbose_name = 'Связанная привычка'
        verbose_name_plural = 'Связанные привычки'

    def __str__(self):
        return f'{self.associated_action}'

    def delete(self, *args, **kwargs):
        self.is_activ = False
        self.save()



class habit_user(models.Model):
    objects = None
    email = models.ForeignKey(User, on_delete=models.CASCADE,  default='mail', verbose_name='почта_пользователя')
    place = models.CharField(max_length=150,  unique=True, default='', verbose_name='место')
    date_of_habit = models.DateTimeField(**NULLABLE, verbose_name='время выполнения привычки')

    action = models.ForeignKey(habit_guide, on_delete=models.CASCADE,  verbose_name='действие', **NULLABLE)
    associated_action = models.ForeignKey(habit_associated, on_delete=models.CASCADE,  verbose_name='связанное действие', **NULLABLE)

    periodicity = models.CharField(max_length=150,  default='Ежедневно', verbose_name='Периодичность')
    reward = models.CharField(max_length=150, default='Благодарность', verbose_name='Вознаграждение')
    time_to_complete = models.DateTimeField(**NULLABLE, verbose_name='время на выполнение привычки')

    is_public = models.BooleanField (default=False, verbose_name='признак публичной привычки')
    is_activ = models.BooleanField(default=True, verbose_name='признак активной привычки')

    class Meta:
        verbose_name = 'Моя привычка'
        verbose_name_plural = 'Мои привычки'

    def __str__(self):
        return f'{self.email}: {self.action}'


    def delete(self, *args, **kwargs):
        self.is_activ = False
        self.save()

