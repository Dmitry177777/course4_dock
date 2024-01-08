
from rest_framework import status
from rest_framework.test import APITestCase


class UserAPITestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def test_create_user(self):
        # Тестирование POST-запроса к API
        data = {
            'email': 'xxxx@mail.ru',
            'telegram_id': '11122233',
            'password': '1234567',
                                }

        response = self.client.post('/users/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class MainTestCase(APITestCase):

    def setUp(self):
        pass

    def test_create_habit(self):
        """Тестирование создание привычки"""

        data = {
            'action': 'чтение',
            'is_useful': True,
            'is_nice': True,
            'is_activ': True
        }

        response = self.client.post(
            '/habit_user/create/',
            data=data
        )

        # print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 1, 'action': 'чтение',
             'is_useful': True, 'is_nice': True, 'is_activ': True}
                         )
