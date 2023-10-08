from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
	def handle (self, *args, **options):


		# очистка модели User
		records = User.objects.all()
		records.delete()


		# создание суперюзера
		user = User.objects.create(
			email='admin@sky.pro',
			first_name = 'admin',
			last_name = 'SkyPro',
			is_staff = True,
			is_superuser = True,
			is_active = True
		)

		user.set_password('admin171717')
		user.save()




		user = User.objects.create(
				email='k1779@mail.ru',
				first_name = 'userMail',
				last_name = 'mailRu',
				is_staff = True,
				is_superuser = False,
				is_active = True
			)

		user.set_password('userMail')
		user.save()



		user = User.objects.create(
			email='k17911971@yandex.ru',
			first_name='userYandex',
			last_name='YandexRu',
			is_staff=True,
			is_superuser=False,
			is_active=True
		)

		user.set_password('userYandex')
		user.save()