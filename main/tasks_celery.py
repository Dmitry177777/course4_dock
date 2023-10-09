from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from  datetime import  datetime, timedelta
from telebot import TeleBot
# from main.telegram_bot import TelegramModule
from main.models import Habit_user, Habit_guide
from users.models import User
from .serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist

# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY)


def send_telegram_confirmation(user_instance):
    try:
        latest_habit_user = Habit_user.objects.filter(email=user_instance).latest('date_of_habit')
        action = latest_habit_user.action
    except ObjectDoesNotExist:
        action = "No action found"

    serializer = UserSerializer(user_instance)
    serialized_user = serializer.data

    message_text = f"Hello {serialized_user['email']}, you have a new habit: {action}."
    send_telegram_message.delay(serialized_user, message_text)






@shared_task
def check_periodicity():
    # Получаем текущую дату
    today = datetime.now().date()
    # Получаем объект Habit_user только активные позиции
    instance = Habit_user.objects.filter(is_activ=True)

    # проходим циклом по всем привычкам
    for  i in instance:
        # Определение разницы даты последнего входа пользователя и текущей даты
        time_diff = today-i.date_of_habit
        tdays = time_diff.days
        # если разница больше запускается уведомление о времени выполнения действия
        if timedelta(days=tdays) > i.periodicity:
            # дата выполнения привычки меняется на текущую
            i.date_of_habit = today
            i.save()
            user_instance = User.objects.filter(email=i.email)
            action=instance.action
            message_text = f"Привет {user_instance.email}, пора выполнить следующее действие: {action}."
            #вызавыется функция рассылки
            send_telegram_message.delay(user_instance, message_text)


@shared_task
def send_telegram_message(serialized_user, message_text):
    try:
        bot.send_message(serialized_user['telegram_id'], message_text)
    except Exception as e:
        # Обработка ошибок отправки сообщения, если необходимо
        print(e)

