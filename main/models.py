from datetime import date
from users.models import User, NULLABLE
import schedule
from django.core.mail import EmailMessage
from django.db import models
from django.urls import reverse

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

    action = models.ForeignKey(habit_guide, to_field='action', on_delete=models.CASCADE,  verbose_name='действие', **NULLABLE)
    associated_action = models.ForeignKey(habit_guide, to_field='action', related_name='associated_action', on_delete=models.CASCADE,  verbose_name='связанное действие', **NULLABLE)

    periodicity = models.DurationField(verbose_name='Периодичность' , **NULLABLE)
    reward = models.CharField(max_length=150, default='Благодарность', verbose_name='Вознаграждение')
    time_to_complete = models.DurationField(**NULLABLE, verbose_name='время на выполнение привычки')

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

