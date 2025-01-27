from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Habit
from unittest.mock import patch

from .serializers import HabitSerializer


class HabitAPITestCase(APITestCase):

    def setUp(self):
        super().setUp()
        Habit.objects.all().delete()
        self.user = get_user_model().objects.create_user(
            username='testuser', email='test@example.com', password='password123'
        )
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place="Тест",
            time="07:00:00",
            action="Тест",
            pleasant_habit=True,
            period=1,
            duration=60,
        )

    @patch('telegram.Bot.get_me')
    def test_create_habit(self):
        # Ваш код для создания привычки
        url = '/habits/'
        data = {
            'place': "test",
            'time': "06:00:00",
            'action': "test",
            'pleasant_habit': True,
            'period': 1,
            'duration': 60,
            'user': self.user.id
        }
        response = self.client.post(url, data, format='json')

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f"Received incorrect status code: {response.status_code}")
        self.assertEqual(response.data['action'], 'test')

    @patch('telegram.Bot.get_me')
    def test_list_habits(self, mock_get_me):
        mock_get_me.return_value = {'id': 12345, 'first_name': 'TestBot'}

        url = '/habits/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    @patch('telegram.Bot.get_me')
    def test_update_habit(self, mock_get_me):
        mock_get_me.return_value = {'id': 12345, 'first_name': 'TestBot'}

        url = f'/habits/{self.habit.id}/'
        data = {'place': "updated_place", 'duration': 120}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 'updated_place')
        self.assertEqual(response.data['duration'], 120)

    @patch('telegram.Bot.get_me')
    def test_delete_habit(self, mock_get_me):
        mock_get_me.return_value = {'id': 12345, 'first_name': 'TestBot'}

        url = f'/habits/{self.habit.id}/'
        response = self.client.delete
