from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import datetime
from telebot import TeleBot
# from main.telegram_bot import TelegramModule
from main.models import Habit_user, Habit_guide
from users.models import User

# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY)

def send_telegram_confirmation(user_instance):
    try:
        # определение новой привычки
        latest_habit_user = Habit_user.objects.filter(email=user_instance).latest('created_at')
        action = latest_habit_user.action  # отфильтрова подписчиков на курс в которм поменялся урок
    except Habit_user.DoesNotExist:
        action = "No action found"  # Handle the case when no Habit_user is found

    message_text = f"Привет {user_instance.email}, у Вас добавлена новая привычка: {action}."
    send_telegram_message.delay(user_instance, message_text)


@shared_task
def check_periodicity():
    #текущее время
    today = datetime.datetime.now()
    Habit_user

    instance = User.objects.all()
    for  i in instance:
        # Определение разницы даты последнего входа пользователя и текущей даты
        time_diff = today-i.last_login
        tdays = time_diff.days
        if tdays > 31:
            i.is_activ = False
            i.save()
            print(f'Пользователь {i.email} не активен уже {tdays} дней. Аккаунт переведен в неактивные')
        message_text = f"Привет {user_instance.email}, у Вас добавлена новая привычка: {action}. Перечень активных привычек: {instance}"
        send_telegram_message.delay(user_instance, message_text)


@shared_task
def send_telegram_message(user_instance, message_text):
    try:
        bot.send_message(user_instance.telegram_id, message_text)
    except Exception as e:
        # Обработка ошибок отправки сообщения, если необходимо
        print(e)



# @shared_task
# def telegram_send(self, *args, **kwargs):
#     bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
#     bot.load_next_step_handlers()  # Загрузка обработчиков
#     bot.infinity_polling()  # Бесконечный цикл бота


# @shared_task
# def send_email_confirmation(lesson, well_id):
#     # определение наименования курса в котором обновлен урок
#     well_name = Well.well_name(pk=well_id)
#     # отфильтровали подписчиков на курс в которм поменялся урок
#     instance = Subscription.objects.filter(well_name_id = well_id)
#
#
#     # рассылка сообщения по подписчикам
#     for i in instance:
#         from_email = i.user.email
#
#         send_mail(
#             subject=f'Урок {lesson} курса {well_name} обновлен',
#             message=f'Мы обновили содержание курса {well_name}, прошу ознакомиться',
#             from_email=from_email,
#             recipient_list=[settings.EMAIL_MODERATOR]
#         )


# @shared_task
# def check_last_login():
#     #текущее время
#     today = datetime.datetime.now()
#
#     instance = User.objects.all()
#     for  i in instance:
#         # Определение разницы даты последнего входа пользователя и текущей даты
#         time_diff = today-i.last_login
#         tdays = time_diff.days
#         if tdays > 31:
#             i.is_activ = False
#             i.save()
#             print(f'Пользователь {i.email} не активен уже {tdays} дней. Аккаунт переведен в неактивные')
#
#
#

# import datetime
#
# # Предположим, что self.last_execution содержит дату последнего выполнения
# # self.periodicity содержит периодичность в днях
#
# # Получаем текущую дату
# current_date = datetime.datetime.now().date()
#
# # Проверяем, была ли последняя выполненная дата
# if self.last_execution is not None:
#     # Вычисляем разницу между текущей датой и последней выполненной датой
#     days_since_last_execution = (current_date - self.last_execution).days
#
#     if days_since_last_execution < 7:
#         raise ValidationError("Действие нельзя выполнять чаще, чем раз в 7 дней.")