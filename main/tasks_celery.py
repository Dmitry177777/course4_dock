from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import datetime

from main.models import Subscription, Well
from users.models import User


@shared_task
def send_email_confirmation(lesson, well_id):
    # определение наименования курса в котором обновлен урок
    well_name = Well.well_name(pk=well_id)
    # отфильтровали подписчиков на курс в которм поменялся урок
    instance = Subscription.objects.filter(well_name_id = well_id)


    # рассылка сообщения по подписчикам
    for i in instance:
        from_email = i.user.email

        send_mail(
            subject=f'Урок {lesson} курса {well_name} обновлен',
            message=f'Мы обновили содержание курса {well_name}, прошу ознакомиться',
            from_email=from_email,
            recipient_list=[settings.EMAIL_MODERATOR]
        )


@shared_task
def check_last_login():
    #текущее время
    today = datetime.datetime.now()

    instance = User.objects.all()
    for  i in instance:
        # Определение разницы даты последнего входа пользователя и текущей даты
        time_diff = today-i.last_login
        tdays = time_diff.days
        if tdays > 31:
            i.is_activ = False
            i.save()
            print(f'Пользователь {i.email} не активен уже {tdays} дней. Аккаунт переведен в неактивные')



