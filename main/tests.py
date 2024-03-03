
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.core.exceptions import ObjectDoesNotExist


from main.views import UserListAPIView
from users.models import User


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        records = User.objects.all()
        records.delete()

        # создание суперюзера
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('admin171717')
        user.save()

        user = User.objects.create(
            email='k1779@mail.ru',
            first_name='userMail',
            last_name='mailRu',
            is_staff=True,
            is_superuser=False,
            is_active=True
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


    def test_create_user(self):
        # Тестирование POST-запроса создание нового пользователя // доступ без аутентификации
        data = {
            "email": "xxxx@mail.ru",
            "telegram_id": "11122233",
            "password": "1234567"
                                }

        response = self.client.post('/user/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_token(self):
        # Тестирование POST-запроса на авторизацию // создание токена пользователя из базы

        data = {
            "email": "k17911971@yandex.ru",
            "password": "userYandex"
                                }

        response = self.client.post('/users/token/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Тестирование POST-запроса на авторизацию // создание токена пользователя которого нет в базе

        data = {
            "email": "k971@yan.ru",
            "password": "urYanx"
        }

        response = self.client.post('/users/token/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_user_list(self, user=None):

        # данные для авторизации пользователя
        data = {
            "email": "k17911971@yandex.ru",
            "password": "userYandex"
        }

        # Авторизация пользователя и получение токена доступа
        response = self.client.post('/users/token/', data)
        access_token = response.data.get('access')



        # Установка заголовка авторизации с токеном доступа
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Отправка Get-запроса на получение списка пользователей
        response = self.client.get('/user/list/')
        # Проверка ответа сервера на доступ к данным
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка соответсвия запрашиваемых данных авторизованному пользователю
        # print(response.data["count"])
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data['count'], 1) # одно значение в выдаче
        self.assertEqual(response.data['results'][0]['email'], data['email']) # значение совпадает с авторизованным пользователем



        # Установка заголовка авторизации без данных токена // пользователь не авторизован
        self.client.credentials(HTTP_AUTHORIZATION=f'')

        # Отправка Get-запроса на получение списка пользователей
        response = self.client.get('/user/list/')
        # Проверка ответа сервера на доступ к данным
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_user_update(self, user=None):

        # данные для авторизации пользователя
        data = {
           "email": "k17911971@yandex.ru",
           "password": "userYandex"
        }

        # Авторизация пользователя и получение токена доступа
        response = self.client.post('/users/token/', data)
        access_token = response.data.get('access')

        # Установка заголовка авторизации с токеном доступа
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        user = User.objects.get(email=data['email'])
        pk=user.pk

        # Обновляемые данные
        updata = {
           "email": "k17911971@yandex.ru",
           "password": "userYandex",
           "phone": "170479",
           "telegram_id": "5418"
        }

        # Отправка Put-запроса на обновление данных пользователя
        response = self.client.put(f'/user/update/{pk}/', updata)
        # Проверка ответа сервера на доступ к данным
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # обновление объекта user
        user = User.objects.get(email=data['email'])

        # Проверка на проведенное обновление
        self.assertEqual(user.phone, updata["phone"])
        self.assertEqual(user.telegram_id, updata["telegram_id"])


        # Проверка соответсвия запрашиваемых данных авторизованному пользователю
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data['id'], pk)  # значение id  в выдаче совпадает с авторизованным пользователем pk

    def test_user_delete(self, user=None):
        # данные для авторизации пользователя
        data = {
            "email": "k17911971@yandex.ru",
            "password": "userYandex"
        }

        # Авторизация пользователя и получение токена доступа
        response = self.client.post('/users/token/', data)
        access_token = response.data.get('access')

        # Установка заголовка авторизации с токеном доступа
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        user = User.objects.get(email=data['email'])
        pk = user.pk
        print(pk)

        # Отправка Del-запроса на удаление данных пользователя
        response = self.client.delete(f'/user/delete/{pk}/', data)
        # Проверка ответа сервера на доступ к данным
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка отсутствия данных пользователя в базе данных
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=pk)
#
# class MainTestCase(APITestCase):
#
#     def setUp(self):
#         pass
#
#     def test_create_habit(self):
#         """Тестирование создание привычки"""
#
#         data = {
#             'action': 'чтение',
#             'is_useful': True,
#             'is_nice': True,
#             'is_activ': True
#         }
#
#         response = self.client.post(
#             '/habit_user/create/',
#             data=data
#         )
#
#         # print(response.json())
#
#         self.assertEqual(
#             response.status_code,
#             status.HTTP_201_CREATED
#         )
#
#         self.assertEqual(
#             response.json(),
#             {'id': 1, 'action': 'чтение',
#              'is_useful': True, 'is_nice': True, 'is_activ': True}
#                          )
