from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied
from tracker.models import Habit
from tracker.paginations import HabitPagination
from tracker.serializers import HabitSerializer
from django.db.models import Q


class HabitViewSet(viewsets.ModelViewSet):
    """ ViewSet для работы с привычками. """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['action', 'place']
    ordering_fields = ['time', 'period']

    def get_queryset(self):
        """ Ограничиваем видимость:
            - только свои привычки
            - публичные привычки других пользователей
        """

        user = self.request.user

        if user.is_anonymous:
            raise PermissionDenied("Пожалуйста, авторизуйтесь для доступа.")

        if self.action == 'list':
            return Habit.objects.filter(Q(user=user) | Q(is_public=True)).distinct()
        return Habit.objects.filter(user=user)