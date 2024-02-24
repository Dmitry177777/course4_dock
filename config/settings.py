"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
# take environment variables from .env.


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.User'


# Application definition

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # install
    'rest_framework',
    'rest_framework_simplejwt',

    # документация
    'drf_yasg',

    # celery
    'django_celery_beat',

    # cors
    'corsheaders',

    # myapp
    'users',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # cors
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
  ]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# take environment variables from .env.
BD_ENGINE = os.environ.get('BD_ENGINE')
BD_NAME = os.environ.get('BD_NAME')
BD_USER = os.environ.get('BD_USER')
BD_PASSWORD = os.environ.get('BD_PASSWORD')
BD_HOST = os.environ.get('BD_HOST')
BD_PORT = os.environ.get('BD_PORT')


DATABASES = {
    'default': {
        'ENGINE': BD_ENGINE,
        'NAME': BD_NAME,
        'USER': BD_USER,
        'PASSWORD': BD_PASSWORD,
        'HOST': BD_HOST,
        'PORT': BD_PORT
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.'
             'password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.'
             'password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.'
             'password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.'
             'password_validation.NumericPasswordValidator', },
]

# Настройки JWT-токенов
# 'rest_framework_simplejwt.authentication.JWTAuthentication',
# 'rest_framework.permissions.AllowAny',
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': []
}


# Настройки срока действия токенов
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

STRIPE_CREATE_URL = 'https://api.stripe.com/v1/payment_intents'
STRIPE_RETRIEVE_URL = ('https://api.stripe.com/v1/'
                       'payment_intents/pi_1Gt09Z2eZvKYlo2C8ZiS4b2r')
STRIPE_AUTH = ('pk_test_51Nnm8HFlTYpLw2PHisnKZg3IOPQIqzPH8YJeZ6L'
               'GBtrBs6IcYJFNukq638cCIg9f6qhnoEVpJwwGBvJCIIo5duPT005Jyp2pZy')


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# redis

CACHES = {
    "default": {
        "BACKEND":	"django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        }
    }

# Настройки для брокера Redis
REDIS_HOST = load_dotenv('REDIS_HOST')
REDIS_PORT = load_dotenv('REDIS_PORT')

# Настройки для Celery
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Настройки для Celery периодические задачи
CELERY_BEAT_SCHEDULE = {
    'check_last_login': {
        'task': 'main.tasks_celery.check_periodicity',  # Путь к задаче
        'schedule': timedelta(minutes=1),
        # Расписание выполнения задачи (например, каждые сутки)
    },
}

# URL-адрес брокера сообщений
CELERY_BROKER_URL = load_dotenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = load_dotenv('CELERY_RESULT_BACKEND')

# Часовой пояс для работы Celery
CELERY_TIMEZONE = "Australia/Tasmania"

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30*60

# CORS
CORS_ALLOWED_ORIGINS = ['https://localhost:8000', ]
# Замените на адрес вашего фронтенд-сервера
# #'http://localhost:8000'
# это адрес вашего фронтенд-сервера.
# Замените его на адрес своего фронтенд-сервера или
# '*' , если вы хотите разрешить запросы от любого домена.

CSRF_TRUSTED_ORIGINS = ["https://read-and-write.example.com", ]
#  Замените на адрес вашего фронтенд-сервера
# и добавьте адрес бэкенд-сервера]

CORS_ALLOW_ALL_ORIGINS = True
