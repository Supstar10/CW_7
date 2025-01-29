from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied
from tracker.models import Habit
from tracker.paginations import HabitPagination
from tracker.serializers import HabitSerializer


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
        """
        user = self.request.user
        if user.is_anonymous:
            raise PermissionDenied("Пожалуйста, авторизуйтесь для доступа.")

        return Habit.objects.filter(user=user).distinct()


class PublicHabitListView(generics.ListAPIView):
    """ Представление для получения списка публичных привычек. """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ всем пользователям (включая анонимных)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['action', 'place']
    ordering_fields = ['time', 'period']
