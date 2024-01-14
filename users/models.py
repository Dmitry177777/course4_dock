from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', gettext_lazy('member')
    MODERATOR = 'moderator', gettext_lazy('moderator')


class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = User(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        assert extra_fields['is_staff']
        assert extra_fields['is_superuser']
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    telegram_id = models.CharField(
        verbose_name='id телеграмм', max_length=200, **NULLABLE)
    password = models.CharField(verbose_name='пароль', max_length=200, )
    is_active = models.BooleanField(default=False)
    role = models.CharField(
        max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    avatar = models.ImageField(
        upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(
        max_length=10, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    pass

# Create your models here.
